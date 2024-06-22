import msgspec

BANNER_DATA_PATH = "./Banners.json"

if __name__ == "__main__":
    try:
        print(f"Reading {BANNER_DATA_PATH}...")
        with open(BANNER_DATA_PATH, "rb") as f:
            banner_data = f.read()
            banner_data_dict = msgspec.json.decode(banner_data)
    except FileNotFoundError:
        print("Banner data file does not exist, can't continue.")
        exit(0)

    new_banner_list = []

    print("Generating new banner list...")
    for banner in banner_data_dict:
        gacha_type = banner["gachaType"]
        banner_type = banner["bannerType"]
        cost_item_id = banner.get("costItemId")
        rateup_5 = banner.get("rateUpItems5")
        rateup_4 = banner.get("rateUpItems4")
        weights_5 = banner.get("weights5")
        weights_4 = banner.get("weights4")

        new_banner = {
            "gacha_type": gacha_type,
            "banner_type": banner_type,
            "cost_item_id": cost_item_id,
            "rateup_5": rateup_5,
            "rateup_4": rateup_4,
            "weights_5": weights_5,
            "weights_4": weights_4,
        }

        new_banner_list.append(new_banner)

    print("Encoding and writing banner list to NewBanners.json...")
    banner_list = msgspec.json.encode(new_banner_list)
    banner_list_formatted = msgspec.json.format(banner_list, indent=4)
    with open("NewBanners.json", "wb") as f:
        f.write(banner_list_formatted)

    print("Done!")
