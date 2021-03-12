import pandas as pd
import re


def filter_data_wos(data: object) -> object:
    data = data.filter(["Full Journal Title", "Article Title", "Addresses"])
    data.rename(columns={"Full Journal Title": "Source Title", "Article Title": "Title", "Addresses": "Affiliations"},
                inplace=True)
    title_list = data["Title"].to_list()
    key_list = []
    for item in title_list:
        reg = re.sub(r'[^A-Za-z0-9]', '', item)
        key_list.append(reg.upper())
    data["KEY"] = key_list
    return data


def filter_data_scopus(data: object) -> object:
    data = data.filter(["Source Title", "Title", "Authors with affiliations"])
    data.rename(columns={"Authors with affiliations": "Affiliations"}, inplace=True)
    title_list = data["Title"].to_list()
    key_list = []
    for item in title_list:
        reg = re.sub(r'[^A-Za-z0-9]', '', item)
        key_list.append(reg.upper())
    data["KEY"] = key_list
    return data


def main():
    total: int = 0

    s1_data = filter_data_scopus(pd.read_excel("s1.xlsx"))
    s2_data = filter_data_scopus(pd.read_excel("s2.xlsx"))
    s3_data = filter_data_scopus(pd.read_excel("s3.xlsx"))
    s4_data = filter_data_scopus(pd.read_excel("s4.xlsx"))
    s_none_data = filter_data_scopus(pd.read_excel("s_none.xlsx"))
    w1_data = filter_data_wos(pd.read_excel("w1.xlsx"))
    w2_data = filter_data_wos(pd.read_excel("w2.xlsx"))
    w3_data = filter_data_wos(pd.read_excel("w3.xlsx"))
    w4_data = filter_data_wos(pd.read_excel("w4.xlsx"))
    w_none_data = filter_data_wos(pd.read_excel("w_none.xlsx"))

    all_data = pd.concat(
        [s1_data, s2_data, s3_data, s4_data, s_none_data, w1_data, w2_data, w3_data, w4_data, w_none_data])

    # Получил 70.xlsx
    w1_data_result = pd.merge(left=all_data, right=w1_data, left_on="KEY", right_on="KEY")
    w1_data_result.rename(
        columns={"Source Title_x": "Source Title", "Title_x": "Title", "Affiliations_x": "Affiliations"}, inplace=True)
    w1_data_result = w1_data_result.filter(["Source Title", "Title", "Affiliations", "KEY"])
    w1_data_to_excel = w1_data_result.drop_duplicates(subset=["KEY"])
    total += len(w1_data_to_excel.index) * 70
    w1_data_to_excel.to_excel("70.xlsx", index=False)

    # Удалил из All 70.xlsx
    all_data_minus_w1 = pd.concat([w1_data_result, all_data])
    all_data_minus_w1.drop_duplicates(keep=False, inplace=True)
    print(f"w1 - {total} all len - {len(all_data_minus_w1.index)}")

    # Получил 50.xlsx
    w2_data_result = pd.merge(left=all_data_minus_w1, right=w2_data, left_on="KEY", right_on="KEY")
    w2_data_result.rename(
        columns={"Source Title_x": "Source Title", "Title_x": "Title", "Affiliations_x": "Affiliations"}, inplace=True)
    w2_data_result = w2_data_result.filter(["Source Title", "Title", "Affiliations", "KEY"])
    w2_data_to_excel = w2_data_result.drop_duplicates(subset=["KEY"])
    total += len(w2_data_to_excel.index) * 50
    all_data_minus_w2 = pd.concat([w2_data_result, all_data_minus_w1])
    all_data_minus_w2.drop_duplicates(keep=False, inplace=True)
    # Добавил в 50.xlsx Scopus
    w2_and_s1_data_result = pd.merge(left=all_data_minus_w2, right=s1_data, left_on="KEY", right_on="KEY")
    w2_and_s1_data_result.rename(
        columns={"Source Title_x": "Source Title", "Title_x": "Title", "Affiliations_x": "Affiliations"}, inplace=True)
    w2_and_s1_data_result = w2_and_s1_data_result.filter(["Source Title", "Title", "Affiliations", "KEY"])
    w2_and_s1_data_to_excel = w2_and_s1_data_result.drop_duplicates(subset=["KEY"])
    total += len(w2_and_s1_data_to_excel .index) * 50
    w2_and_s1_data_to_excel = w1_data_result.drop_duplicates()
    w2_and_s1_data_to_excel.to_excel("50.xlsx", index=False)
    # Удалил из All 50.xlsx
    all_data_minus_w2_and_s1 = pd.concat([w2_and_s1_data_result, all_data_minus_w2])
    all_data_minus_w2_and_s1.drop_duplicates(keep=False, inplace=True)
    print(f"w2 and s1 - {total} all len - {len(all_data_minus_w2_and_s1.index)}")

    # Получил 30.xlsx
    s2_data_result = pd.merge(left=all_data_minus_w2_and_s1, right=s2_data, left_on="KEY", right_on="KEY")
    s2_data_result.rename(
        columns={"Source Title_x": "Source Title", "Title_x": "Title", "Affiliations_x": "Affiliations"}, inplace=True)
    s2_data_result = s2_data_result.filter(["Source Title", "Title", "Affiliations", "KEY"])
    s2_data_to_excel = s2_data_result.drop_duplicates(subset=["KEY"])
    total += len(s2_data_to_excel.index) * 30
    s2_data_to_excel.to_excel("30.xlsx", index=False)
    # Удалил из All 30.xlsx
    all_data_minus_s2 = pd.concat([s2_data_result, all_data_minus_w2_and_s1])
    all_data_minus_s2.drop_duplicates(keep=False, inplace=True)
    print(f"w2 - {total} all len - {len(all_data_minus_s2.index)}")

    # Получил 25.xlsx
    w3_data_result = pd.merge(left=all_data_minus_s2, right=w3_data, left_on="KEY", right_on="KEY")
    w3_data_result.rename(
        columns={"Source Title_x": "Source Title", "Title_x": "Title", "Affiliations_x": "Affiliations"}, inplace=True)
    w3_data_result = w3_data_result.filter(["Source Title", "Title", "Affiliations", "KEY"])
    w3_data_to_excel = w3_data_result.drop_duplicates(subset=["KEY"])
    total += len(w3_data_to_excel.index) * 25
    w3_data_to_excel.to_excel("25.xlsx", index=False)
    # Удалил из All 25.xlsx
    all_data_minus_w3 = pd.concat([w3_data_result, all_data_minus_s2])
    all_data_minus_w3.drop_duplicates(keep=False, inplace=True)
    print(f"w3 - {total} all len - {len(all_data_minus_w3.index)}")

    # Получил 18.xlsx
    w4_data_result = pd.merge(left=all_data_minus_w3, right=w4_data, left_on="KEY", right_on="KEY")
    w4_data_result.rename(
        columns={"Source Title_x": "Source Title", "Title_x": "Title", "Affiliations_x": "Affiliations"}, inplace=True)
    w4_data_result = w4_data_result.filter(["Source Title", "Title", "Affiliations", "KEY"])
    w4_data_to_excel = w4_data_result.drop_duplicates(subset=["KEY"])
    total += len(w4_data_to_excel.index) * 18
    w4_data_to_excel.to_excel("18.xlsx", index=False)
    # Удалил из All 18.xslx
    all_data_minus_w4 = pd.concat([w4_data_result, all_data_minus_w3])
    all_data_minus_w4.drop_duplicates(keep=False, inplace=True)
    print(f"w4 - {total} all len - {len(all_data_minus_w4.index)}")

    # Получил 15.xlsx
    s3_data_result = pd.merge(left=all_data_minus_w4, right=s3_data, left_on="KEY", right_on="KEY")
    s3_data_result.rename(
        columns={"Source Title_x": "Source Title", "Title_x": "Title", "Affiliations_x": "Affiliations"}, inplace=True)
    s3_data_result = s3_data_result.filter(["Source Title", "Title", "Affiliations", "KEY"])
    s3_data_to_excel = s3_data_result.drop_duplicates(subset=["KEY"])
    total += len(s3_data_to_excel.index) * 15
    s3_data_to_excel.to_excel("15.xlsx", index=False)
    # Удалил из All 15.xslx
    all_data_minus_s3 = pd.concat([s3_data_result, all_data_minus_w4])
    all_data_minus_s3.drop_duplicates(keep=False, inplace=True)
    print(f"s3 - {total} all len - {len(all_data_minus_s3.index)}")

    # Получил 9.xlsx
    s4_data_result = pd.merge(left=all_data_minus_s3, right=s4_data, left_on="KEY", right_on="KEY")
    s4_data_result.rename(
        columns={"Source Title_x": "Source Title", "Title_x": "Title", "Affiliations_x": "Affiliations"}, inplace=True)
    s4_data_result = s4_data_result.filter(["Source Title", "Title", "Affiliations", "KEY"])
    s4_data_to_excel = s4_data_result.drop_duplicates(subset=["KEY"])
    total += len(s4_data_to_excel.index) * 9
    s4_data_to_excel.to_excel("9.xlsx", index=False)
    # Удалил из All 9.xslx
    all_data_minus_s4 = pd.concat([s4_data_result, all_data_minus_s3])
    all_data_minus_s4.drop_duplicates(keep=False, inplace=True)
    print(f"s4 - {total} all len - {len(all_data_minus_s4.index)}")

    # Получил 7.xlsx
    all_data_minus_s4 = all_data_minus_s4.drop_duplicates(subset=["KEY"])
    total += len(all_data_minus_s4.index) * 7
    print(f"all - {total} all len - {len(all_data_minus_s4.index)}")
    all_data_minus_s4.to_excel("7.xlsx", index=False)
