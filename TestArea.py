def test(z):
    try:
        if z / 40:
            try:
                if z.isfloat():
                    print('ok')
                else:
                    print('ok')
            except ValueError:
                print('yes')
