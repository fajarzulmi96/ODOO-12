{
    'name':'Module Custome Pembelian',
    'author' : 'Fajar Zulmi Sopian',
    'version' : '15.0.1.0.0',
    'category' : 'purchase',
    'summary' : 'Module Custom Pembelian',
    'descripttion' : """
        Ini adalah module custom By Fajar Zulmi Sopian
    """,
    'website' : '',
    'depends' : ['web','base','product','stock'],
    'data' : [
        'security/ir.model.acces.csv',
        'views/fajar_pembelian_view.xml',
        'views/fajar_pembelian_action.xml',
        'views/fajar_pembelian_menuitem.xml',
        'view/fajar_pembelian_sequence.xml',
        'view/fajar_pembelian_cron.xml',
        'reports/fajar_pembelian_qweb.xml',
        'reports/fajar_pembelian_qrcode.xml'
    ],
    'installable' : True,
    'application' : True,
    'license' : 'OEEL-1',
}