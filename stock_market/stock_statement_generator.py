from datetime import datetime
#stock_statement_generator which will produce a statement with actions and stock actions in clear time line format

#  test input is given
# I assum the timestamps of actions in input is always from first to latest
actions = [{'date': '1992/07/14 11:12:30', 'action': 'BUY', 'price': '12.3', 'ticker': 'AAPL', 'shares': '500'}]
stock_actions = [{'date': '1992/08/14', 'dividend': '0.10', 'split': '', 'stock': 'AAPL'}, {'date': '1992/09/01', 'dividend': '', 'split': '3', 'stock': 'AAPL'}]


#functions to return the string outputs
#Input num number of share bought with price price  
def buy(stock, num, price):
   return("    - You bought {} shares of {} at a price of ${} per share".format(num, stock, price))

#Input num number of share sold with price price, and the final total profit
def sell(stock, num, price, profit):
    return("    - You sold {} shares of {} at a price of ${} per share for a profit of ${}".format(num, stock, price, profit))

#Input dividend d_price for each share of the stock
def dividend(stock, num, d_price):
    return("    - {} paid out ${} dividend per share, and you have {} shares".format(stock, d_price, num))

#Input stock name, split number, and final number of shares
def split(stock, s_num, c_num):
    return("    - {} split {} to 1, and you have {} shares".format(stock, s_num, c_num))
 
#Input actions with index i and stock_action with index j
#return earliest datetime in all actions
def earliest(actions, stock_actions, i, j):
    if i < len(actions) and j < len(stock_actions):
        datetime_act = datetime.strptime(actions[i].get('date'), '%Y/%m/%d %H:%M:%S')
        datetime_sto_act = datetime.strptime(stock_actions[j].get('date'), '%Y/%m/%d')
        date = None

        if datetime_act < datetime_sto_act :
            date = datetime_act
        else:
            date = datetime_sto_act
        return date 

    elif i >= len(actions) and j < len(stock_actions):
        datetime_sto_act = datetime.strptime(stock_actions[j].get('date'), '%Y/%m/%d')
        date = datetime_sto_act
        return date

    elif i < len(actions) and j >= len(stock_actions):
        datetime_act = datetime.strptime(actions[i].get('date'), '%Y/%m/%d %H:%M:%S')
        date = datetime_act
        return date

def complete(actions, stock_actions, i, j):
    if i < len(actions) and j < len(stock_actions):
        return False
    elif i >= len(actions) and j < len(stock_actions):
        return False
    elif i < len(actions) and j >= len(stock_actions):
        return False
    else:
        return True

#Print/Return the stcok_statement to output
#Input actions and stock actions
def generate_stat(actions, stock_actions):
    i = 0
    j = 0 
    if_complete = False
    #keep all kinds of stocks here
    all_stocks = []
    #the total decidend 
    total_devidend = 0

    while not if_complete:
        
        transactions = []
        
        #get actions during the earliest day
        date = earliest(actions, stock_actions, i, j)

        print("On {}-{}-{}, you have:".format(date.year, date.month, date.day))
        
        # apply the actions
        for act in actions:
            datetime_act = datetime.strptime(act.get('date'), '%Y/%m/%d %H:%M:%S')
            if datetime_act.year == date.year and datetime_act.month == date.month and datetime_act.day == date.day:
                if act.get('action') == 'BUY':
                    #add stock to all_stocks
                    buy_price = str(format(float(act['price']), '.2f'))
                    exist = False
                    #check this kind of stock's existance
                    for stock in all_stocks:
                        if stock['ticker'] == act['ticker']:
                            c_shares = float(stock['shares'])
                            new_shares = float(act['shares'])
                            c_price = float(stock['price'])
                            new_price = float(act['price'])
                            total = c_shares + new_shares
                            stock['price'] = str((c_shares*c_price + new_shares*new_price)/(c_shares + new_shares))
                            stock['shares'] = str(total)
                            exist = True
                    if not exist:
                        all_stocks.append({'price': buy_price, 'ticker': act['ticker'], 'shares': act['shares']})
                        
                    transactions.append(buy(act['ticker'], act['shares'], buy_price))

                if act.get('action') == 'SELL':
                    #minus shares of stocks and calculate profit
                    for stock in all_stocks:
                        if stock['ticker'] == act['ticker']:
                            stock['shares'] = str(int(float(stock['shares']) - float(act['shares'])))
                    for k in range(len(all_stocks)):
                        if int(all_stocks[k]['shares']) == 0:
                            del all_stocks[k]
                
                    profit = format((float(act['price']) - float(stock['price'])) * float(act['shares']), '.2f')
                    transactions.append(sell(act['ticker'], act['shares'], format(float(act['price']), '.2f'), profit))
                i+=1
        # apply the stock actions
        for sto_act in stock_actions:
            datetime_act2 = datetime.strptime(sto_act.get('date'), '%Y/%m/%d')
            if datetime_act2.year == date.year and datetime_act2.month == date.month and datetime_act2.day == date.day:
                if sto_act.get('dividend') != '':
                    # get number of shares of this stock
                    for stock in all_stocks:
                        if stock['ticker'] == sto_act['stock']:
                            number_shares = int(stock['shares'])
                    transactions.append(dividend(sto_act['stock'], number_shares, sto_act['dividend']))
                    # add profit to total dividend
                    total_devidend += number_shares * float(sto_act['dividend'])

                if sto_act.get('split') != '':
                    #edit the total number of shares
                    for stock in all_stocks:
                        if stock['ticker'] == sto_act['stock']:
                            number_shares_s = int(stock['shares'])
                            number_split = number_shares_s * float(sto_act['split'])
                            stock['shares'] = str(int(number_split))
                            stock['price'] = str(format(number_shares_s * float(stock['price'])/ number_split, '.2f'))
                    
                    transactions.append(split(sto_act['stock'], sto_act['split'], number_split))

                j+=1
                
        for stock in all_stocks:
            print("    - {} shares of {} at ${} per share".format(stock['shares'],stock['ticker'], format(float(stock['price']), '.2f'))) 

        print("    - ${} of dividend income".format(format(total_devidend, '.2f')))
        
        print(" Transactions:")
        for tran in transactions:
            print(tran)
        
        if_complete = complete(actions, stock_actions, i, j)
            
    return None
            


if __name__ == '__main__':
    #some detail tests:
    # datetime_act = datetime.strptime(actions[0].get('date'), '%Y/%m/%d %H:%M:%S')
    # datetime_sto_act = datetime.strptime(stock_actions[0].get('date'), '%Y/%m/%d')
    # date = None
    # if datetime_act < datetime_sto_act:
    #     date = datetime_act
    # else:
    #     date = datetime_sto_act

    # print("On {}-{}-{}, you have:".format(date.year, date.month, date.day))
    # reault = complete(actions, stock_actions, 1, 2)
    # print(reault)
    
    #test stock statement generator for ouput 
    # if we delete the last action(a dictinary here) of stock_actions the output will be exactly the same to given one
    actions = [{'date': '1992/07/14 11:12:30', 'action': 'BUY', 'price': '12.3', 'ticker': 'AAPL', 'shares': '500'}, {'date': '1992/09/13 11:15:20', 'action': 'SELL', 'price': '15.3', 'ticker': 'AAPL', 'shares': '100'}, {'date': '1992/10/14 15:14:20', 'action': 'BUY', 'price': '20', 'ticker': 'MSFT', 'shares': '300'}, {'date': '1992/10/17 16:14:30', 'action': 'SELL', 'price': '20.2', 'ticker': 'MSFT', 'shares': '200'}, {'date': '1992/10/19 15:14:20', 'action': 'BUY', 'price': '21', 'ticker': 'MSFT', 'shares': '500'}, {'date': '1992/10/23 16:14:30', 'action': 'SELL', 'price': '18.2', 'ticker': 'MSFT', 'shares': '600'}, {'date': '1992/10/25 10:15:20', 'action': 'SELL', 'price': '20.3', 'ticker': 'AAPL', 'shares': '300'}, {'date': '1992/10/25 16:12:10', 'action': 'BUY', 'price': '18.3', 'ticker': 'MSFT', 'shares': '500'}]
    stock_actions = [{'date': '1992/08/14', 'dividend': '0.10', 'split': '', 'stock': 'AAPL'}, {'date': '1992/09/01', 'dividend': '', 'split': '3', 'stock': 'AAPL'}, {'date': '1992/10/15', 'dividend': '0.20', 'split': '', 'stock': 'MSFT'},{'date': '1992/10/16', 'dividend': '0.20', 'split': '', 'stock': 'ABC'}]
    
    generate_stat(actions, stock_actions)
