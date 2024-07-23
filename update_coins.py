from api_coins_data.manager import start_update_coins_data


if __name__ == '__main__':
    try:
        start_update_coins_data()
    except Exception as err:
        print(f"\nERROR: {err}")
