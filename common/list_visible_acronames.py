from common.usb_switch import list_visible_acronames

if __name__ == '__main__':
    visible_acronames = list_visible_acronames()
    print(f"Visible acronames number: {len(visible_acronames)}")
    print(f"Visible acronames: {', '.join(visible_acronames)}")
