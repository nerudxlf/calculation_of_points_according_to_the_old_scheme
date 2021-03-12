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


def get_result(all_data: object, w_data: object, num, file_name, total):
    data_result = pd.merge(left=all_data, right=w_data, left_on="KEY", right_on="KEY")
    data_result.rename(
        columns={"Source Title_x": "Source Title", "Title_x": "Title", "Affiliations_x": "Affiliations"}, inplace=True)
    data_result = data_result.filter(["Source Title", "Title", "Affiliations", "KEY"])
    data_to_excel = data_result.drop_duplicates(subset=["KEY"])
    total += len(data_to_excel.index) * num
    data_to_excel.to_excel(file_name, index=False)
    all_data_minus = pd.concat([data_result, all_data])
    all_data_minus.drop_duplicates(keep=False, inplace=True)
    print(f"w1 - {total} all len - {len(all_data_minus.index)}")
    return total, all_data_minus


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
    total, all_data = get_result(all_data, w1_data, 70, "70.xlsx", total)
    # Получил 50.xlsx
    w2_data_result = pd.merge(left=all_data, right=w2_data, left_on="KEY", right_on="KEY")
    w2_data_result.rename(
        columns={"Source Title_x": "Source Title", "Title_x": "Title", "Affiliations_x": "Affiliations"}, inplace=True)
    w2_data_result = w2_data_result.filter(["Source Title", "Title", "Affiliations", "KEY"])
    w2_data_to_excel = w2_data_result.drop_duplicates(subset=["KEY"])
    total += len(w2_data_to_excel.index) * 50
    all_data_minus_w2 = pd.concat([w2_data_result, all_data])
    all_data_minus_w2.drop_duplicates(keep=False, inplace=True)
    # Добавил в 50.xlsx Scopus
    w2_and_s1_data_result = pd.merge(left=all_data_minus_w2, right=s1_data, left_on="KEY", right_on="KEY")
    w2_and_s1_data_result.rename(
        columns={"Source Title_x": "Source Title", "Title_x": "Title", "Affiliations_x": "Affiliations"}, inplace=True)
    w2_and_s1_data_result = w2_and_s1_data_result.filter(["Source Title", "Title", "Affiliations", "KEY"])
    w2_and_s1_data_to_excel = w2_and_s1_data_result.drop_duplicates(subset=["KEY"])
    total += len(w2_and_s1_data_to_excel .index) * 50
    w2_and_s1_data_to_excel = all_data.drop_duplicates()
    w2_and_s1_data_to_excel.to_excel("50.xlsx", index=False)
    # Удалил из All 50.xlsx
    all_data_minus_w2_and_s1 = pd.concat([w2_and_s1_data_result, all_data_minus_w2])
    all_data_minus_w2_and_s1.drop_duplicates(keep=False, inplace=True)
    print(f"w2 and s1 - {total} all len - {len(all_data_minus_w2_and_s1.index)}")
    all_data = all_data_minus_w2_and_s1

    # Получил 30.xlsx
    total, all_data = get_result(all_data, s2_data, 30, "30.xlsx", total)

    # Получил 25.xlsx
    total, all_data = get_result(all_data, w3_data, 30, "25.xlsx", total)

    # Получил 18.xlsx
    total, all_data = get_result(all_data, w4_data, 18, "18.xlsx", total)

    # Получил 15.xlsx
    total, all_data = get_result(all_data, s3_data, 15, "15.xlsx", total)

    # Получил 9.xlsx
    total, all_data = get_result(all_data, s4_data, 9, "9.xlsx", total)

    # Получил 7.xlsx
    all_data_minus_s4 = all_data.drop_duplicates(subset=["KEY"])
    total += len(all_data_minus_s4.index) * 7
    print(f"all - {total} all len - {len(all_data_minus_s4.index)}")
    all_data_minus_s4.to_excel("7.xlsx", index=False)
