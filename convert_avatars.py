import msgspec

AVATAR_EXCEL_DATA_PATH = "./AvatarExcelConfigData.json"
AVATAR_SKILL_DEPOT_PATH = "./AvatarSkillDepotExcelConfigData.json"
AVATAR_SKILL_EXCEL_PATH = "./AvatarSkillExcelConfigData.json"

decoder = msgspec.json.Decoder()

quality_to_stars = {
    "QUALITY_ORANGE_SP": 5,  # Aloy rarity
    "QUALITY_ORANGE": 5,
    "QUALITY_PURPLE": 4,
    "QUALITY_BLUE": 3,
    "QUALITY_GREEN": 2,
    # There is no mention of 1* color anywhere in excel datas
}


def find_energy_skill(skill_depot: dict, skill_depot_id: int):
    for skill in skill_depot:
        if skill["id"] == skill_depot_id:
            return skill.get("energySkill")


def find_element(skill_excel: dict, skill_excel_id: int):
    for skill in skill_excel:
        if skill["id"] == skill_excel_id:
            if skill["costElemType"] == "Electric":
                return "Elect"
            return skill["costElemType"]


if __name__ == "__main__":
    try:
        print(f"Reading {AVATAR_EXCEL_DATA_PATH}...")
        with open(AVATAR_EXCEL_DATA_PATH, "rb") as f:
            avatar_excel = f.read()
            avatar_excel_dict = decoder.decode(avatar_excel)

        print(f"Reading {AVATAR_SKILL_DEPOT_PATH}...")
        with open(AVATAR_SKILL_DEPOT_PATH, "rb") as f:
            skill_depot = f.read()
            skill_depot_dict = decoder.decode(skill_depot)

        print(f"Reading {AVATAR_SKILL_EXCEL_PATH}...")
        with open(AVATAR_SKILL_EXCEL_PATH, "rb") as f:
            skill_excel = f.read()
            skill_excel_dict = decoder.decode(skill_excel)
    except FileNotFoundError as e:
        print(f"Some files are missing, can't continue: {e}")
        exit(0)

    new_avatar_list = []

    print("Generating new avatar list...")
    for avatar in avatar_excel_dict:
        av_id = avatar["id"]

        # We ignore test characters
        if av_id <= 10000001 or av_id >= 11000000:
            continue

        av_icon_name = avatar["iconName"]
        quality_type = avatar["qualityType"]
        name_hash = avatar["nameTextMapHash"]
        desc_hash = avatar["descTextMapHash"]

        skill_depot_id = avatar["skillDepotId"]
        energy_skill = find_energy_skill(skill_depot_dict, skill_depot_id)
        element = find_element(skill_excel_dict, energy_skill)

        av_name = '_'.join(av_icon_name.split("_")[2:])
        gacha_img = "UI_Gacha_AvatarImg_"+av_name+".png"

        new_avatar = {
            "id": av_id,
            "avatar_name": av_name,
            "quality": quality_to_stars[quality_type],
            "name_text_map_hash": name_hash,
            "desc_text_map_hash": desc_hash,
            "element": element,
            "gacha_img": gacha_img
        }

        new_avatar_list.append(new_avatar)

    print("Encoding and writing avatar list to AvatarData.json...")
    avatar_list = msgspec.json.encode(new_avatar_list)
    avatar_list_formatted = msgspec.json.format(avatar_list, indent=4)
    with open("./output/AvatarData.json", "wb") as f:
        f.write(avatar_list_formatted)

    print("Done!")
