import pandas as pd


def get_data(file='test.csv'):
    with open(file, "rb") as f:
        data = pd.read_csv(f, header=None, sep=",")
    # print(data)
    # print(data[0].min())
    # print(data[1].max())
    return data


def main():
    data = get_data()
    lenx = abs(int(data[0].max())) + abs(data[0].min())
    leny = abs(int(data[1].max())) + abs(data[1].min())
    print(lenx)
    print(leny)


if __name__ == "__main__":
    main()
