from twocaptcha import TwoCaptcha

api_key = '4257cd460f13b1ccad5b64138f58ece7'


def solve():
    solver = TwoCaptcha(api_key)

    try:
        result = solver.recaptcha(
            sitekey='6LfSEDIbAAAAAEyHtxj2xtEA8It6gSi6s4_PNxwI',
            url='https://coinmarketcap.com/',
            invisible=1)
        return result
    except Exception as e:
        # sys.exit(e)
        return 'error'

    # else:
    #     sys.exit('solved: ' + str(result))

if __name__ == '__main__':
    print(solve())
