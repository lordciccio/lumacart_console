
import requests
url = 'http://localhost:8000/hooks/woo/new_order'
payload = """{
   "order":{
      "id":612,
      "order_number":612,
      "order_key":"wc_order_56dc9cf09391c",
      "created_at":"2016-03-06T21:11:12Z",
      "updated_at":"2016-03-06T21:11:12Z",
      "completed_at":"2016-03-06T21:11:12Z",
      "status":"processing",
      "currency":"EUR",
      "total":"0.20",
      "subtotal":"0.20",
      "total_line_items_quantity":1,
      "total_tax":"0.00",
      "total_shipping":"0.00",
      "cart_tax":"0.00",
      "shipping_tax":"0.00",
      "total_discount":"0.00",
      "shipping_methods":"Europe Flat Rate",
      "payment_details":{
         "method_id":"cod",
         "method_title":"Cash on Delivery",
         "paid":false
      },
      "billing_address":{
         "first_name":"Ebeto",
         "last_name":"Ebetini",
         "company":"Transustazia",
         "address_1":"via sile 41",
         "address_2":"",
         "city":"Roncade",
         "state":"VE",
         "postcode":"31056",
         "country":"IT",
         "email":"mzaccariotto@h-umus.it",
         "phone":"45442424"
      },
      "shipping_address":{
         "first_name":"Ebeto",
         "last_name":"Ebetini",
         "company":"Transustazia",
         "address_1":"via sile 41",
         "address_2":"",
         "city":"Roncade",
         "state":"VE",
         "postcode":"31056",
         "country":"IT"
      },
      "note":"ancora ancora, ne voglio!!!",
      "customer_ip":"151.95.16.236",
      "customer_user_agent":"Mozilla\\/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit\\/601.4.4 (KHTML, like Gecko) Version\\/9.0.3 Safari\\/601.4.4",
      "customer_id":0,
      "view_order_url":"http:\\/\\/www.lumacart.com\\/my-account\\/view-order\\/612",
      "line_items":[
         {
            "id":5,
            "subtotal":"0.20",
            "subtotal_tax":"0.00",
            "total":"0.20",
            "total_tax":"0.00",
            "price":"0.20",
            "quantity":1,
            "tax_class":null,
            "name":"Test item",
            "product_id":609,
            "sku":"varsku000",
            "meta":[
               {
                  "key":"pa_color",
                  "label":"Color",
                  "value":"Beige"
               },
               {
                  "key":"pa_size",
                  "label":"Size",
                  "value":"XL"
               }
            ]
         }
      ],
      "shipping_lines":[
         {
            "id":6,
            "method_id":"flat_rate",
            "method_title":"Europe Flat Rate",
            "total":"0.00"
         }
      ],
      "tax_lines":[

      ],
      "fee_lines":[

      ],
      "coupon_lines":[

      ],
      "customer":{
         "id":0,
         "email":"mzaccariotto@h-umus.it",
         "first_name":"Ebeto",
         "last_name":"Ebetini",
         "billing_address":{
            "first_name":"Ebeto",
            "last_name":"Ebetini",
            "company":"Transustazia",
            "address_1":"via sile 41",
            "address_2":"",
            "city":"Roncade",
            "state":"VE",
            "postcode":"31056",
            "country":"IT",
            "email":"mzaccariotto@h-umus.it",
            "phone":"45442424"
         },
         "shipping_address":{
            "first_name":"Ebeto",
            "last_name":"Ebetini",
            "company":"Transustazia",
            "address_1":"via sile 41",
            "address_2":"",
            "city":"Roncade",
            "state":"VE",
            "postcode":"31056",
            "country":"IT"
         }
      }
   }
}"""

r = requests.post(url, data=payload)
