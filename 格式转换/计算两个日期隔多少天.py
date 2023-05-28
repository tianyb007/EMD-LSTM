
from datetime import date

start_date = date(2020, 9, 12)   # 2020年9月12日
end_date = date(2021, 6, 12)     # 2021年6月12日

delta = end_date - start_date    # 两个日期相减得到间隔天数
days = delta.days

print(f'2020年9月12日到2021年6月12日共有{days}天')
# 2020年9月12日到2021年6月12日共有276天