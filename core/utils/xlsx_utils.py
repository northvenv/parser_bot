import xlsxwriter
import io

async def create_excel_file(data):
    buffer = io.BytesIO()
    name_columns = [
            ('Название', 'A1'),
            ('Ссылка на товар', 'B1'), 
            ('Цена', 'C1'),
        ]

    workbook = xlsxwriter.Workbook(buffer)
    worksheet = workbook.add_worksheet()
    worksheet.set_row(0, 20)

    bold = workbook.add_format({'bold': True, 'align':'center'})
    counter = 0
    for field_data in name_columns:
        name, field = field_data
        worksheet.set_column(counter, counter, 80)
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
    buffer.seek(0)


    content = buffer.getvalue()
    buffer.close()

    return content
