import logging

# log config
logging.basicConfig(format="[%(asctime)s] %(name)s %(levelname)s: %(message)s", level=logging.INFO,
                    datefmt="%Y-%m-%d %I:%M:%S")
text_handle_log = logging.getLogger("text_handle_module")


def count_day(datas: dict) -> set:
    """
    :param datas: response data
    :return: clock in date
    """
    text_handle_log.info("处理考勤文本")
    result = set()
    for data in datas['data']:
        # data["dateYmd"] = '2023-12-04'
        date = int(data['dateYmd'].split("-")[-1])
        result.add(date)
    return result


def run(arg):
    print(count_day(arg))


if __name__ == '__main__':
    run('')
