trains = {
    "G1001": {
        "start": "上海",
        "end": "南京",
        "price": 145,
        "seat": 30
    },
    "G1002": {
        "start": "上海",
        "end": "杭州",
        "price": 95,
        "seat": 50
    },
    "G1003": {
        "start": "上海",
        "end": "北京",
        "price": 680,
        "seat": 20
    }
}

orders = []


def show_menu():
    print("========== 高铁订票系统 ==========")
    print("1. 查看所有车次")
    print("2. 查询车次")
    print("3. 购买车票")
    print("4. 查看我的订单")
    print("5. 退票")
    print("6. 统计收入")
    print("7. 退出")
    print("=================================")


def show_trains():
    print(f"{'车次':<8}{'起点':<8}{'终点':<8}{'票价':<8}{'剩余座位':<8}")
    for train_id, info in trains.items():
        print(f"{train_id:<8}{info['start']:<8}{info['end']:<8}{info['price']:<8}{info['seat']:<8}")


def search_train():
    end = input("请输入终点：")
    print(f"{'车次':<8}{'起点':<8}{'终点':<8}{'票价':<8}{'剩余座位':<8}")
    found = False
    for train_id, info in trains.items():
        if info['end'] == end:
            print(f"{train_id:<8}{info['start']:<8}{info['end']:<8}{info['price']:<8}{info['seat']:<8}")
            found = True
    if not found:
        print(f"没有到{end}的列车。")


def buy_ticket():
    name = input("姓名：")
    id_card = input("身份证：")
    train_id = input("车次：")
    count = int(input("购买数量："))

    if train_id not in trains:
        print("车次不存在！")
        return

    train_info = trains[train_id]
    if count <= 0:
        print("购买数量必须大于0！")
        return

    if train_info['seat'] < count:
        print("余票不足！")
        return

    train_info['seat'] -= count
    money = train_info['price'] * count

    order = {
        "name": name,
        "id": id_card,
        "train": train_id,
        "count": count,
        "money": money
    }
    orders.append(order)
    print(f"购票成功！\n{name} 购买了 {train_id} {count}张，共{money}元")


def show_orders():
    if not orders:
        print("暂无订单")
        return
    for order in orders:
        print(f"{order['name']}\n{order['train']}\n{order['count']}张\n{order['money']}元\n")


def refund():
    id_card = input("请输入身份证：")
    found_index = -1
    for i, order in enumerate(orders):
        if order['id'] == id_card:
            found_index = i
            break

    if found_index == -1:
        print("未找到订单！")
        return

    order = orders[found_index]
    train_id = order['train']
    count = order['count']

    if train_id in trains:
        trains[train_id]['seat'] += count

    del orders[found_index]
    print(f"退票成功！已恢复{count}张座位。")


def count_money():
    total_orders = len(orders)
    total_money = sum(order['money'] for order in orders)
    total_seat = sum(train['seat'] for train in trains.values())

    print(f"今日订单：{total_orders}")
    print(f"销售额：{total_money}")
    print(f"剩余座位：{total_seat}")


def main():
    while True:
        show_menu()
        choice = input("请选择功能（1-7）：")
        if choice == '1':
            show_trains()
        elif choice == '2':
            search_train()
        elif choice == '3':
            buy_ticket()
        elif choice == '4':
            show_orders()
        elif choice == '5':
            refund()
        elif choice == '6':
            count_money()
        elif choice == '7':
            print("感谢使用高铁订票系统，再见！")
            break
        else:
            print("输入错误，请重新选择！")
        print()


if __name__ == "__main__":
    main()