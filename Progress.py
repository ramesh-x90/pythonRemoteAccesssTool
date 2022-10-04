def bar(s1 , s2  , prograss , max , barsize , unit):
    
    p = 1
    if unit == "b":
        p = 0

    if unit == "kB":
        p = 1

    if unit == "MB":
        p = 2

    if unit == "GB":
        p = 3   

    fill = prograss / max

    print('\r' + s1+ " " +
            s2 + " " + str(int( fill* 100)) + "% |" +

            '\33[107m' +
            " " * round( fill * barsize) +
            '\33[0m' +
            " " * int(barsize - fill * barsize) +

            "|" + str(round( ( prograss/pow(2,10*p )  ) , 2)) + "/" +str(round( (max/pow(2,10*p)) , 2)) + " "+ unit +
            " [ ]", end=""
        )