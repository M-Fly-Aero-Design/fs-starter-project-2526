from pymavlink import mavutil

def connect(connection_string='udp:127.0.0.1:14540'):
    """
    Connect to the MAVLink system.
    """
    try:
        master = mavutil.mavlink_connection(connection_string)
        master.wait_heartbeat()
        print("Heartbeat from system (system %u component %u)" % (master.target_system, master.target_component))
        return master
    except Exception as e:
        print(f"Failed to connect: {e}")

master = connect()

def set_mode(master, mode):
    """
    Source: https://discuss.px4.io/t/mav-cmd-do-set-mode-all-possible-modes/8495/2
    Manual: base_mode:217, main_mode:1, sub_mode:0
    Stabilized: base_mode:209, main_mode:7, sub_mode:0
    Acro: base_mode:209, main_mode:5, sub_mode:0
    Rattitude: base_mode:193, main_mode:8, sub_mode:0
    Altitude: base_mode:193, main_mode:2, sub_mode:0
    Offboard: base_mode:209, main_mode:6, sub_mode:0
    Position: base_mode:209, main_mode:3, sub_mode:0
    Hold: base_mode:217, main_mode:4, sub_mode:3
    Mission: base_mode:157, main_mode:4, sub_mode:4
    Return: base_mode:157, main_mode:4, sub_mode:5
    Follow me: base_mode:157, main_mode:4, sub_mode:8
    Missing: LAND, RTGS, TAKEOFF
    """
    MODE_DICTIONARY = {
        "MANUAL": (217, 1, 0),
        "STABILIZED": (209, 7, 0),
        "ACRO": (209, 5, 0),
        "RATTITUDE": (193, 8, 0),
        "ALTCTL": (193, 2, 0),
        "OFFBOARD": (209, 6, 0),
        "POSCTL": (209, 3, 0),
        "LOITER": (217, 4, 3),
        "MISSION": (157, 4, 4),
        "RTL": (157, 4, 5),
        "FOLLOWME": (157, 4, 8),
        "LAND": (157, 4, 6),  # Assuming LAND is similar to RTL
        "RTGS": (157, 4, 7),  # Assuming RTGS is similar to RTL
        "TAKEOFF": (209, 4, 1)  # Assuming TAKEOFF is similar to POSCTL
    }
    if mode not in MODE_DICTIONARY:
        print(f"Unknown mode: {mode}")
        print("Available modes:", MODE_DICTIONARY)
        return

    base_mode, main_mode, sub_mode = MODE_DICTIONARY[mode]
    print(f"Setting mode: {mode} (base_mode: {base_mode}, main_mode: {main_mode}, sub_mode: {sub_mode})")

    master.mav.command_long_send(
        master.target_system, master.target_component,
        mavutil.mavlink.MAV_CMD_DO_SET_MODE, 0,
        base_mode, main_mode, sub_mode, 0, 0, 0, 0)

    # Check mode
    current_mode = master.flightmode
    if current_mode == mode:
        print(f"Mode set to {mode}")
    else:
        print(f"Failed to set mode. Current mode is {current_mode}")

# set_mode(master, "RTL")
from pymavlink.dialects.v20 import common as mavlink2
def upload_mission(master, waypoints=[(47.397742, 8.545594, 10), (47.397872, 8.546050, 10)]):
    """
    waypoints: (lat [deg], lon [deg], alt [m])
    """
    # Example mission: 2 waypoints
    mission_items = [
        {
            "seq": i,
            "frame": mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
            "command": mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,
            "current": 0,
            "autocontinue": 1,
            "param1": 0, "param2": 0, "param3": 0, "param4": 0,
            "x": lat, "y": lon, "z": alt
        }
        for i, (lat, lon, alt) in enumerate(waypoints)
    ]

    # Step 1: Clear existing mission
    master.mav.mission_clear_all_send(master.target_system, master.target_component)

    # Step 2: Send MISSION_COUNT
    master.mav.mission_count_send(master.target_system, master.target_component, len(mission_items))

    # Step 3: Handle MISSION_REQUEST_INT and send each MISSION_ITEM_INT
    for _ in mission_items:
        msg = master.recv_match(type='MISSION_REQUEST_INT', blocking=True, timeout=5)
        if msg is None:
            print("Timeout waiting for MISSION_REQUEST_INT")
            break

        i = msg.seq
        item = mission_items[i]

        master.mav.mission_item_int_send(
            master.target_system,
            master.target_component,
            item["seq"],
            item["frame"],
            item["command"],
            item["current"],
            item["autocontinue"],
            item["param1"], item["param2"],
            item["param3"], item["param4"],
            int(item["x"] * 1e7),
            int(item["y"] * 1e7),
            item["z"]
        )
        print(f"Sent mission item {i}")

    # Step 4: Wait for MISSION_ACK
    ack = master.recv_match(type='MISSION_ACK', blocking=True, timeout=5)
    if ack:
        print("Mission upload successful")
    else:
        print("Timeout waiting for MISSION_ACK")

def param_set(master, name, value, type=mavutil.mavlink.MAV_PARAM_TYPE_REAL32):
    """
    https://docs.px4.io/main/en/advanced_config/parameter_reference.html
    """
    master.mav.param_set_send(
        master.target_system, master.target_component,
        name.encode('utf-8'), value, type)
    print(f"Parameter {name} set to {value}")

# param_set(master, "MIS_TKO_LAND_REQ", 0, mavutil.mavlink.MAV_PARAM_TYPE_INT32)  # Example parameter setting

upload_mission(master)