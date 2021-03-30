import pandas as pd
import re


def rename_and_filter_df(data: object) -> object:
    data.rename(
        columns={"Source Title_x": "Source Title", "Title_x": "Title", "Affiliations_x": "Affiliations"}, inplace=True)
    return data.filter(["Source Title", "Title", "Affiliations", "KEY"])


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


def get_result(all_data: object, w_data: object, num: int, file_name: str, total: int) -> (int, object):
    data_result = pd.merge(left=all_data, right=w_data, left_on="KEY", right_on="KEY")
    data_result = rename_and_filter_df(data_result)
    total += len(data_result.index) * num
    data_result.to_excel(file_name, index=False)
    all_data_minus = pd.concat([data_result, all_data])
    all_data_minus.drop_duplicates(keep=False, inplace=True, subset=["KEY"])
    return total, all_data_minus


def get_result_50(all_data: object, w_data: object, s_data: object, num: int, file_name: str,
                  total: int) -> (int, object):
    data_result = pd.merge(left=all_data, right=w_data, left_on="KEY", right_on="KEY")
    data_result = rename_and_filter_df(data_result)
    total += len(data_result.index) * num
    data_result.to_excel("w"+file_name, index=False)
    all_data_minus_w = pd.concat([data_result, all_data])
    all_data_minus_w.drop_duplicates(keep=False, inplace=True, subset=["KEY"])
    w_and_s_data_result = pd.merge(left=all_data_minus_w, right=s_data, left_on="KEY", right_on="KEY")
    w_and_s_data_result = rename_and_filter_df(w_and_s_data_result)
    total += len(w_and_s_data_result.index) * num
    w_and_s_data_result.to_excel("s"+file_name, index=False)
    all_data_minus_w_and_s = pd.concat([w_and_s_data_result, all_data_minus_w])
    all_data_minus_w_and_s.drop_duplicates(keep=False, inplace=True, subset=["KEY"])
    return total, all_data_minus_w_and_s


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
    
    all_data = all_data.drop_duplicates(subset=["KEY"])
    print(f"all len {len(all_data.index)}")
    total, all_data = get_result(all_data, w1_data, 70, "70.xlsx", total)
    print(f"w1 - {total} all len - {len(all_data.index)}")

    total, all_data = get_result_50(all_data, w2_data, s1_data, 50, "50.xlsx", total)
    print(f"w2 and s1 - {total} all len - {len(all_data.index)}")

    total, all_data = get_result(all_data, s2_data, 30, "30.xlsx", total)
    print(f"s2 - {total} all len - {len(all_data.index)}")

    total, all_data = get_result(all_data, w3_data, 25, "25.xlsx", total)
    print(f"w3 - {total} all len - {len(all_data.index)}")

    total, all_data = get_result(all_data, w4_data, 18, "18.xlsx", total)
    print(f"w4 - {total} all len - {len(all_data.index)}")

    total, all_data = get_result(all_data, s3_data, 15, "15.xlsx", total)
    print(f"s3 - {total} all len - {len(all_data.index)}")

    total, all_data = get_result(all_data, s4_data, 9, "9.xlsx", total)
    print(f"s4 - {total} all len - {len(all_data.index)}")

    all_data_minus_s4 = all_data.drop_duplicates(subset=["KEY"])
    total += len(all_data_minus_s4.index) * 7
    print(f"all - {total} all len - {len(all_data_minus_s4.index)}")
    all_data_minus_s4.to_excel("7.xlsx", index=False)
