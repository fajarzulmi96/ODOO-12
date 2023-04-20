import json
import requests
from odoo.tests import Form
import werkzeug .wrappers

from odoo import odoo,models,fields, _
from odoo import http, _, exceptions
from odoo.http import content_disposition, request
import id
import xlsxwriter

class ReportExcelFajarPembelianController(http,Controller):

    @http.route(['/fajar_pembelian/fajar_pembelian_report_excel/<model("fajar.pembelian"):data>',],type='http', auth="user", csrf=False)
    def get_fajar_pembelian_excel_report(self, data=none, **args):
        response = request.make_response(
            None,
            headers = [
                ('Content-Type', 'application/vnd.ms-excel'),
                ('Content-Disposition', content_disposition('Fajar Pembelian Report' + '.xlsx'))
            ]
        )

        #Buat Object workbook dari Library xlsxwriter
        output = io.BytesIO()
        workbook = xlsxwriter.workbook(output, {'in_memory' : True})

        #Buat Style untuk mengatur jenis font,ukuran font, border dan alligment
        atas.style = workbook.add_format({'font_name' : 'Times', 'bold' : True, 'align' : 'left'})
        atas.isi_style = workbook.add.format({'font_name' : 'Times', 'bold' : True, 'align' : 'left'})
        header.style = workbook.add.format({'font_name' : 'Times', 'bold' : True, 'left' : 1, 'bottom' : 1, 'top' : 1, 'right' : 1, 'align' : 'center'})
        text.style = workbook.add.format({'font_name' : 'Times', 'bold' : False, 'left' : 1, 'bottom' : 1, 'top' : 1, 'right' : 1, 'align' : 'left'})
        number.style = workbook.add.format({'font_name' : 'Times', 'bold' : True, 'left' : 1, 'bottom' : 1, 'top' : 1, 'right' : 1, 'align' : 'center'})

        #looping modul fajar pembelian yyang di pilih
        for atas in data:
            #buat worksheet tab per user
            sheet = workbook.add.worksheet(atas.name)
            #set orientation jadi landscape
            sheet.set_landscape()
            #set ukuran kertas dengan angka 9 yang artinya kertas A4
            sheet.set_paper(9)
            #set margin kertas dalam satuan inchi
            sheet.set_margins(0.5, 0.5, 0.5, 0.5)
            #set lebar kolom
            sheet.set_column('A:A', 5)
            sheet.set_column('B:B', 55)
            sheet.set_column('C:C', 48)
            sheet.set_column('D:D', 15)
            sheet.set_column('E:E', 15)
            sheet.set_column('F:F', 25)
            sheet.set_column('G:G', 25)
            #set judul atas
            sheet.merge_range('A1:B1', 'Name', atas_style)
            sheet.merge_range('A2:B2', 'Date', atas_style) 
            #set isi atas
            sheet.write(0, 2, atas.name, atas_isi_style)
            sheet.write(1, 2, atas.date, atas_isi_style)
            #set judul table
            sheet.write(3, 0, 'No', header_style)
            sheet.write(3, 1, 'Product', header_style)
            sheet.write(3, 2, 'Description', header_style)
            sheet.write(3, 3, 'Quantity', header_style)
            sheet.write(3, 4, 'Uom', header_style)
            sheet.write(3, 5, 'Price', header_style)
            sheet.write(3, 6, 'Sub Total', header_style)

            row = 4
            number = 1

            #cari record data fajar pembelian line yang dipilih user
            record_line = request.env['fajar.pembelian.line'].search([('fajar_pembelian_id', '=', atas.id)])
            for line in record_line:
                #content / isi tabel
                sheet.write(row, 0, number, text_style)
                sheet.write(row, 1, line.product_id.display_name, text_style)
                sheet.write(row, 2, line.description, text_style)
                sheet.write(row, 3, line.quantity, text_style)
                sheet.write(row, 4, line.uom_id.name, text_style)
                sheet.write(row, 5, line.price, text_style)
                sheet.write(row, 6, line.sub_total, text_style)

                row += 1
                number += 1
        
        #Memasukan file excel yang sudah di generate ke response dan return
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
        return response

class FajarPembelianRestAPI(http.Controller):
    
    @http.route(['/api/fajar_pembelian_get/'], type='http', auth='public', methods=['GET'], csrf=False)
    def fajar_pembelian_resapi_get(self, **params):
        fajar_pembelian = request.env['fajar.pembelian'].sudo().search([])
        # get_id = params.get("id")
        fajar_pembelian = request.env['fajar.pembelian'].sudo().search(['id', '=', get_id])
        dict_fajar_pembelian = {}
        data_fajar_pembelian = []
        for h in fajar_pembelian:
            dict_brand = {}
            detail_brand = []
            dict_detail_product = {}
            detail_product = []
            for b in h.brand_ids:
                dict_brand = {'id' : b.id,'name': b.name}
                detail_brand.append(dict_brand)
            for p in h.fajar_pembelian_ids:
                dict_detail_product = {'product_id' : p.product_id.display_name, 'description' : p.description, 'quantity' : p.quanttity, 
                                        'uom_id' : p.uom_id.name, 'price' : p.price, 'sub_total' : p.sub_total}
                detail_product.append(dict_detail_product)
            dict_fajar_pembelian = {'id' : h.id, 'name' : h.name, 'brand_ids' : detail_brand, 'fajar_pembelian_ids' : detail_product}
            data_fajar_pembelian.append(dict_fajar_pembelian)
        data = {
            'status' : 200,
            'message' : 'succes',
            'response' : data_fajar_pembelian,
        }
        try:
            return werkzeug.wrappers.Response(
                status = 200,
                content_type = 'applcation/json; charset = utf-8',
                response = json.dumps(data)
            )
        except:
            return werkzeug.wrappers.Response(
                status = 400,
                content_type = 'application/json; charset= utf-8',
                headers = [('Acces-Control-Allow-Origin', '*')]
                response = json.dumps({
                    'error' : 'Error',
                    'error_descrip' : 'Error Description',
                }))
    
class FajarPembelianRestAPI(http.Controller):
    @http.route(['/api/fajar_pembelian_post/'], type='http', auth='public', methods=['POST'], csrf=False)
    def fajar_pembelian_resapi_post(self, **params):
        order = params.get("order")
        tanggal = order[0]['tanggal']
        brand_ids = order[0]['brand_ids']
        name_brand = []
        for a in brand_ids:
            name_brand.append(a['name'])
        brands_obj = request.env['fajar.brand'].sudo().search([('name', 'in', name_brand)])
        fajar_pembelian_ids = order [0]['fajar_pembelian_ids']