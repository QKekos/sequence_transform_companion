
from sequence_transform_companion.hid_listener import DeviceListener
from sequence_transform_companion.observers import PrintObserver, MissedRulesObserver


def main():
    """Acquire debugging information from usb hid devices"""
    print_observer = PrintObserver()
    missed_rules_observer = MissedRulesObserver()

    device_finder = DeviceListener([
        print_observer, missed_rules_observer
    ])

    print("Looking for devices...", flush=True)
    device_finder.run_forever()


if __name__ == "__main__":
    main()
