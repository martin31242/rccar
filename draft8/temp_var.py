def auto_logoff():
    while tempvar.count_time_logoff < 600:
        tempvar.count_time_logoff += 1
        print(tempvar.count_time_logoff)
        time.sleep(1)
    motor_stop()
    return exit()


def notresponding():
    while tempvar.count_time_stop_if_not_responding < 5:
        tempvar.count_time_stop_if_not_responding += 1
        print(tempvar.count_time_stop_if_not_responding)
        time.sleep(1)
    motor_stop()


    # tt1 = Thread(target=auto_logoff)
    # tt2 = Thread(target=notresponding)
    # tt1.daemon = True
    # tt2.daemon = True
    # tt1.start()
    # tt2.start()