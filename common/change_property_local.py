import argparse
import sys

from common import config



try:
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--section", help="property section")
    parser.add_argument("-p", "--property", help="property name")
    parser.add_argument("-v", "--value", help="property value")
    args = parser.parse_args()

    for key, attrib in args.__dict__.items():
        args.__setattr__(key, attrib.upper())

    settings = config.CommonConfig.get_instance()
    prev_value = settings.config.get(args.section, args.property)

    print(f"Current value of [{args.section}][{args.property}] is {prev_value}")
    print(f"Changing value of [{args.section}][{args.property}] to {args.value}")

    settings.set_value_in_section(args.section, args.property, args.value)

    config_updated = config.CommonConfig._read_config()

    updated_value = config_updated.get(args.section, args.property)
    print(f"Updated value of [{args.section}][{args.property}] is {updated_value}")

except Exception as e:
    print(f"Exception occurred: {e}")
    sys.exit(1)
