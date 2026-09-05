from stock_universe import STOCK_UNIVERSE


STOCK_UNIVERSITY = ["PAYFIN","PAYRETAIL","PAYINFRA","PAYGOLD","PAYBOND","PAYTECH"]  

{"bull" :"With an expected return of {r:.1%} against a beta of {b:.2f}, this offers attractive risk-adjdusted upside",
"bear" :"std_dev as a risk" }

print("Final Summary combining both bull and bear perspectives for each stock:")
for stock in STOCK_UNIVERSITY:
    if stock == "PAYFIN":
        r = STOCK_UNIVERSE[stock]["analyst_expected_return"]
        b = STOCK_UNIVERSE[stock]["beta"] 
        std = STOCK_UNIVERSE[stock]["std_dev"] 
        print(f"bull: With an expected return of {r:.1%} against a beta of {b:.2f}, this offers attractive risk-adjdusted upside",
              f"bear: std_dev as a risk of {std:.2%}")  

        print(f"synthesizer: Balancing return potential ({r:.1%}) against volatility ({std:.2%}), {stock} presents a balanced opportunity")
    elif stock == "PAYRETAIL":       
        r = STOCK_UNIVERSE[stock]["analyst_expected_return"]
        b = STOCK_UNIVERSE[stock]["beta"] 
        std = STOCK_UNIVERSE[stock]["std_dev"]
        print(f"bull: With an expected return of {r:.1%} against a beta of {b:.2f}, this offers attractive risk-adjdusted upside",
              f"bear: std_dev as a risk of {std:.2%}")
        print(f"synthesizer: Balancing return potential ({r:.1%}) against volatility ({std:.2%}), {stock} presents a balanced opportunity")
    elif stock == "PAYINFRA": 
        r = STOCK_UNIVERSE[stock]["analyst_expected_return"]
        b = STOCK_UNIVERSE[stock]["beta"] 
        std = STOCK_UNIVERSE[stock]["std_dev"] 
        print(f"bull: With an expected return of {r:.1%} against a beta of {b:.2f}, this offers attractive risk-adjdusted upside",
              f"bear: std_dev as a risk of {std:.2%}")
        print(f"synthesizer: Balancing return potential ({r:.1%}) against volatility ({std:.2%}), {stock} presents a balanced opportunity")
    elif stock == "PAYGOLD":        
        r = STOCK_UNIVERSE[stock]["analyst_expected_return"]
        b = STOCK_UNIVERSE[stock]["beta"] 
        std = STOCK_UNIVERSE[stock]["std_dev"]
        print(f"bull: With an expected return of {r:.1%} against a beta of {b:.2f}, this offers attractive risk-adjdusted upside",
                f"bear: std_dev as a risk of {std:.2%}")
        print(f"synthesizer: Balancing return potential ({r:.1%}) against volatility ({std:.2%}), {stock} presents a balanced opportunity")
    elif stock == "PAYBOND":
        r = STOCK_UNIVERSE[stock]["analyst_expected_return"]
        b = STOCK_UNIVERSE[stock]["beta"] 
        std = STOCK_UNIVERSE[stock]["std_dev"]      
        print(f"bull: With an expected return of {r:.1%} against a beta of {b:.2f}, this offers attractive risk-adjdusted upside",
              f"bear: std_dev as a risk of {std:.2%}")
        print(f"synthesizer: Balancing return potential ({r:.1%}) against volatility ({std:.2%}), {stock} presents a balanced opportunity")
    elif stock == "PAYTECH":
        r = STOCK_UNIVERSE[stock]["analyst_expected_return"]
        b = STOCK_UNIVERSE[stock]["beta"] 
        std = STOCK_UNIVERSE[stock]["std_dev"]  
        print(f"bull: With an expected return of {r:.1%} against a beta of {b:.2f}, this offers attractive risk-adjdusted upside",
              f"bear: std_dev as a risk of {std:.2%}")
        print(f"synthesizer: Balancing return potential ({r:.1%}) against volatility ({std:.2%}), {stock} presents a balanced opportunity")
 
