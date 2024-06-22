import msgspec

WEAPON_EXCEL_DATA_PATH = "./WeaponExcelConfigData.json"

if __name__ == "__main__":
    try:
        print(f"Reading {WEAPON_EXCEL_DATA_PATH}...")
        with open(WEAPON_EXCEL_DATA_PATH, "rb") as f:
            weapon_excel = f.read()
            weapon_excel_dict = msgspec.json.decode(weapon_excel)
    except FileNotFoundError:
        print("Weapon data file does not exist, can't continue.")
        exit(0)

    new_weapon_list = []

    print("Generating new weapon list...")
    for weapon in weapon_excel_dict:
        weapon_id = weapon["id"]
        weapon_type = weapon["icon"].split("_")[2]
        weapon_rank = weapon["rankLevel"]
        name_hash = weapon["nameTextMapHash"]
        desc_hash = weapon["descTextMapHash"]

        weapon_icon_name = '_'.join(weapon["icon"].split("_")[3:])
        gacha_img = f"UI_Gacha_EquipIcon_{weapon_type}_{weapon_icon_name}.png"

        new_weapon = {
            "id": weapon_id,
            "weapon_type": weapon_type,
            "rank": weapon_rank,
            "name_text_map_hash": name_hash,
            "desc_text_map_hash": desc_hash,
            "weapon_name": weapon_icon_name,
            "gacha_img": gacha_img
        }

        new_weapon_list.append(new_weapon)

    print("Encoding and writing weapon list to WeaponData.json...")
    weapon_list = msgspec.json.encode(new_weapon_list)
    weapon_list_formatted = msgspec.json.format(weapon_list, indent=4)
    with open("./output/WeaponData.json", "wb") as f:
        f.write(weapon_list_formatted)

    print("Done!")
