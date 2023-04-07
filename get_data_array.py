import json

import pandas as pd


def data_file():
    original_data = [(1.2358771562576294, 0.8885444402694702), (6.086360454559326, 1.0427088737487793),
                     (5.936509132385254, 4.022181510925293), (1.1873016357421875, 3.7481889724731445),
                     (1.2530081272125244, 0.9054474234580994), (1.2584795951843262, 0.8969888091087341)]
    pdo_data = pd.DataFrame(original_data)
    with open("abc.txt", "w+") as f1:
        pdo_data.to_csv(f1, index=None, header=["x", "y"], line_terminator="\n")


def file_data():
    with open("abc.txt", "r") as f2:
        get_data = pd.read_csv(f2)
        # print(get_data)
        # final_data = get_data.to_numpy()
        # final_data = get_data.to_json()
        # print(final_data)
        # for item in final_data:
        #     for x, y in item:
        #         print(x, y)
        points = []
        for row in get_data.iterrows():
            # print(row[1]['x'])
            points.append((row[1]["x"], row[1]["y"]))
        print(points)


if __name__ == "__main__":
    file_data()
