import EmpClient

client=EmpClient.EmpClient()

a=client.connected()
if a=='1':
    b=client.login("000002","new_psw2")
    print(b)
    # b=client.change_psw("psw2","new_psw2",)
    # print(b)
    b=client.get_info("000002")
    print(b)

    b=client.get_record_and_state("2018-08","111111")
    print(b)

    # b=client.add_emp_info("000007","name7","department7","photo7")
    # print(b)


client.close()
# while True:
#     pass