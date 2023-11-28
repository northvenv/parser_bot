import xlsxwriter
import aioredis
from core.utils.redis_utils import ConnectRedis, create_redis_pool





async def create_excel_file(data, product):
    excel_file = f'{product}.xlsx'

    name_columns = [
            ('Название', 'A1'),
            ('Ссылка на товар', 'B1'), 
            ('Цена', 'C1'),
        ]

    workbook = xlsxwriter.Workbook(excel_file)
    worksheet = workbook.add_worksheet()
    worksheet.set_row(0, 40)

    bold = workbook.add_format({'bold': True, 'align':'center'})
    counter = 0
    for field_data in name_columns:
        name, field = field_data
        worksheet.set_column(counter, counter, 40)
        worksheet.write(field, name, bold)
        counter += 1
    row = 1
    for product in data:
        col_number = 0
        for i in range(len(product)):
            worksheet.write(row, col_number, product[i])
            col_number += 1
        row += 1
    workbook.close()
    # global redis
    # await setup_redis()
    # with open(f'{product}.xlsx', 'rb') as f:
    #     content = f.read()
    pool = create_redis_pool()
    redis = ConnectRedis(pool)
    await redis.redis_set(f'{product}_file', excel_file)
