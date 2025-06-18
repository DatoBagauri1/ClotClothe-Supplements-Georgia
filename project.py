from flask import Flask, render_template, request, redirect, session, url_for,flash
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from flask import flash


app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
users = {}

products = [
    {
        "name": "Optimum Nutrition Gold Standard 100% Whey",
        "desc": "24g of protein per serving to support muscle recovery. Available in Chocolate and Vanilla.",
        "price": "170 ₾ (2 lbs) / 300 ₾ (5 lbs)",
        "image": "https://content.optimumnutrition.com/i/on/on-gold-standard-100-whey-protein_Image_01?$TTL_PRODUCT_IMAGES$&locale=en-us,en-gb,*&w=509&sm=aspect&aspect=1:1&fmt=webp"
    },
    {
        "name": "MuscleTech Nitro-Tech Whey Gold",
        "desc": "30g of protein with added creatine and BCAAs for enhanced muscle growth.",
        "price": "180 ₾ (2 lbs) / 320 ₾ (5 lbs)",
        "image": "https://th.bing.com/th/id/R.b13ae8606709a4964e5260112e95eaf9?rik=ho5r%2b7JsZ9L%2f5g&pid=ImgRaw&r=0"
    },
    {
        "name": "BSN Syntha-6 Protein Powder",
        "desc": "22g of ultra-premium protein matrix with 10g of essential amino acids per serving.",
        "price": "160 ₾ (2.91 lbs) / 290 ₾ (5 lbs)",
        "image": "https://th.bing.com/th/id/R.fd673be7feb7b0257298b6f51031fa71?rik=MRGBP%2f9fi4yoaA&pid=ImgRaw&r=0"
    },
    {
        "name": "Dymatize ISO100 Hydrolyzed",
        "desc": "25g of hydrolyzed 100% whey protein isolate for fast absorption and digestion.",
        "price": "200 ₾ (1.6 lbs) / 350 ₾ (5 lbs)",
        "image": "https://th.bing.com/th/id/OIP.h3T1nk-zNuvM01NrrCUr0gHaHa?w=186&h=186&c=7&r=0&o=5&dpr=1.3&pid=1.7"
    },
    {
        "name": "Cellucor C4 Original Pre-Workout",
        "desc": "150mg caffeine and 1.6g beta-alanine per serving to boost energy and endurance.",
        "price": "120 ₾ (30 servings)",
        "image": "https://th.bing.com/th/id/OIP.W79tm2JUsNHPjgM1ktcisAHaHa?w=186&h=186&c=7&r=0&o=5&dpr=1.3&pid=1.7"
    },
    {
        "name": "Universal Nutrition Animal Pak",
        "desc": "Comprehensive multivitamin and performance supplement with over 60 key ingredients.",
        "price": "140 ₾ (44 packs)",
        "image": "https://tse1.mm.bing.net/th/id/OIP.uqAiiJQGYixBeh8gCEPx6wHaHa?rs=1&pid=ImgDetMain"
    },
    {
        "name": "Myprotein Impact Whey Protein",
        "desc": "21g of high-quality whey protein concentrate per serving, available in various flavors.",
        "price": "150 ₾ (2.2 lbs) / 270 ₾ (5.5 lbs)",
        "image": "https://th.bing.com/th/id/OIP.9SsWjRxER3yE-EUS4CngnAHaHa?w=192&h=192&c=7&r=0&o=5&dpr=1.3&pid=1.7"
    },
    {
        "name": "GHOST Whey Protein",
        "desc": "25g of whey protein blend with digestive enzymes, available in unique flavors like Oreo.",
        "price": "190 ₾ (2 lbs)",
        "image": "https://th.bing.com/th/id/OIP.2ar-kpYzJwRMUBg0-m8zlwHaHa?w=207&h=207&c=7&r=0&o=5&dpr=1.3&pid=1.7"
    },
    {
        "name": "Applied Nutrition Critical Mass",
        "desc": "High-calorie mass gainer with 42g protein and 600+ calories per serving.",
        "price": "220 ₾ (6 lbs)",
        "image": "https://th.bing.com/th/id/OIP.jWv78yNeyWnVtMHgr7-T4AHaHa?w=184&h=184&c=7&r=0&o=5&dpr=1.3&pid=1.7"
    },
    {
        "name": "Optimum Nutrition Micronized Creatine Monohydrate",
        "desc": "5g of pure creatine monohydrate per serving to enhance strength and performance.",
        "price": "70 ₾ (300g) / 130 ₾ (600g)",
        "image": "https://th.bing.com/th/id/R.bc43ed98006171cb055ea38149358a15?rik=r6l4AXOOahoj3A&riu=http%3a%2f%2fcdn.grofers.com%2fapp%2fimages%2fproducts%2fsliding_image%2f530138a.jpg%3fts%3d1703941489&ehk=ubyJTe%2bgS0ErPj4DN8GYJBlbtoASwVRhsHXtVhYYfFI%3d&risl=&pid=ImgRaw&r=0"
    },
    {
        "name": "Mutant Mass Extreme 2500",
        "desc": "High-calorie gainer with 56g protein, 255g carbs per serving for serious mass gainers.",
        "price": "240 ₾ (15 lbs)",
        "image": "https://th.bing.com/th/id/OIP.oD89BpazuCBdB6PacEoVVQAAAA?w=178&h=180&c=7&r=0&o=5&dpr=1.3&pid=1.7"
    },
    {
        "name": "Rule 1 R1 Protein",
        "desc": "25g of fast-absorbing whey protein isolate & hydrolysate. No creamers, no gums.",
        "price": "190 ₾ (2 lbs) / 330 ₾ (5 lbs)",
        "image": "https://tse2.mm.bing.net/th/id/OIP.LCfCzWZxpQwYp0fuTnuc5wHaHa?rs=1&pid=ImgDetMain"
    },




      {
    "name": "Optimum Nutrition Serious Mass",
    "desc": "High-calorie weight gainer with 1,250 calories and 50g protein per serving, plus 25 vitamins and minerals.",
    "price": "200 ₾ (6 lbs) / 350 ₾ (12 lbs)",
    "image": "https://th.bing.com/th/id/OIP.8MkYoACTtspPcDpPKyycRAHaHa?w=179&h=180&c=7&r=0&o=5&dpr=1.3&pid=1.7"
  },
  {
    "name": "Optimum Nutrition Gold Standard Pre-Workout",
    "desc": "175mg caffeine, 3g creatine, and 1.5g beta-alanine to boost energy and focus before workouts.",
    "price": "130 ₾ (30 servings)",
    "image": "https://th.bing.com/th/id/OIP.UeTNBQl1-u3OsmsS2JkNYQHaHa?w=180&h=180&c=7&r=0&o=5&dpr=1.3&pid=1.7"
  },
  {
    "name": "Optimum Nutrition Amino Energy + Electrolytes",
    "desc": "5g amino acids with 100mg caffeine and electrolytes for energy, focus, and hydration.",
    "price": "120 ₾ (30 servings)",
    "image": "https://th.bing.com/th/id/OIP.8HbYkDrp2kiybCz5Xk-XYwHaMG?w=119&h=194&c=7&r=0&o=5&dpr=1.3&pid=1.7"
  },
  {
    "name": "Optimum Nutrition Micronized Creatine Powder",
    "desc": "5g pure creatine monohydrate per serving to support muscle strength and power.",
    "price": "80 ₾ (300g)",
    "image": "https://th.bing.com/th/id/OIP.D5I_58x0DQsQsm7heKh2kQHaHg?w=194&h=197&c=7&r=0&o=5&dpr=1.3&pid=1.7"
  },
  {
    "name": "Optimum Nutrition Gold Standard 100% Casein",
    "desc": "24g slow-digesting micellar casein protein per serving, ideal for nighttime recovery.",
    "price": "180 ₾ (2 lbs) / 320 ₾ (4 lbs)",
    "image": "https://th.bing.com/th/id/OIP.VyLzghCaBK3d8Wt7jSjY1QHaHa?w=195&h=195&c=7&r=0&o=5&dpr=1.3&pid=1.7"
  },
  {
    "name": "Ghost Legend Pre-Workout",
    "desc": "Pre-workout with 250mg caffeine, 4g citrulline, and 2g beta-alanine for energy and endurance.",
    "price": "140 ₾ (30 servings)",
    "image": "https://th.bing.com/th/id/OIP.MsbrTD8SXjhfWd0MCSP2MgHaHa?w=190&h=190&c=7&r=0&o=5&dpr=1.3&pid=1.7"
  },
  {
    "name": "Ghost Pump",
    "desc": "Stimulant-free pre-workout with 4g citrulline and 2g arginine nitrate for muscle pumps.",
    "price": "130 ₾ (40 servings)",
    "image": "https://th.bing.com/th/id/OIP.SxMIyXNZLFJn2DqZycw6LAHaHa?w=170&h=180&c=7&r=0&o=5&dpr=1.3&pid=1.7"
  },
  {
    "name": "Ghost Energy Drink",
    "desc": "Ready-to-drink energy beverage with 200mg caffeine and nootropics for focus.",
    "price": "10 ₾ (473ml can)",
    "image": "https://th.bing.com/th/id/OIP.xnnmLe-HgcxS66aRL9N_8gHaHa?w=186&h=186&c=7&r=0&o=5&dpr=1.3&pid=1.7"
  },
  {
    "name": "Ghost Vegan Protein",
    "desc": "20g plant-based protein per serving, available in flavors like Pancake Batter and Banana Pancake.",
    "price": "180 ₾ (2 lbs)",
    "image": "https://tse1.mm.bing.net/th/id/OIP.f3sqT8lCrsnT2C52LROhgwHaHa?rs=1&pid=ImgDetMain"
  },
  {
    "name": "Ghost Hydration",
    "desc": "Electrolyte-rich hydration supplement with sodium, potassium, and magnesium.",
    "price": "100 ₾ (40 servings)",
    "image": "https://th.bing.com/th/id/OIP.CRIbrwtZsHZb_o3OSmPPqwHaHa?w=200&h=200&c=7&r=0&o=5&dpr=1.3&pid=1.7"
  },
  {
    "name": "MuscleTech Nitro-Tech",
    "desc": "30g protein with 3g creatine per serving to support muscle growth and strength.",
    "price": "190 ₾ (2 lbs) / 340 ₾ (4 lbs)",
    "image": "https://th.bing.com/th/id/OIP.pZA3S30DKE1uhRQlinmS5wHaHa?w=195&h=194&c=7&r=0&o=5&dpr=1.3&pid=1.7"
  },
  {
    "name": "MuscleTech Cell-Tech Creatine",
    "desc": "Creatine formula with 5g creatine and 38g carbs per serving for enhanced absorption.",
    "price": "150 ₾ (3 lbs)",
    "image": "https://th.bing.com/th/id/OIP.ZOAMByD09s3IVpEA_PlK3AHaKj?w=134&h=190&c=7&r=0&o=5&dpr=1.3&pid=1.7"
  },
  {
    "name": "MuscleTech Hydroxycut Hardcore Elite",
    "desc": "Thermogenic fat burner with 270mg caffeine and green coffee extract.",
    "price": "120 ₾ (100 capsules)",
    "image": "https://th.bing.com/th/id/OIP.ZrGfZLFnjo7ATJzDzdu_qQHaHa?w=194&h=194&c=7&r=0&o=5&dpr=1.3&pid=1.7"
  },
  {
    "name": "MuscleTech Platinum 100% Glutamine",
    "desc": "5g micronized glutamine per serving to support muscle recovery.",
    "price": "90 ₾ (300g)",
    "image": "https://ncrfoodsupplements.com/wp-content/uploads/2023/11/MUSCLETECH_GLUTAMINE-1.jpeg"
  },
  {
    "name": "MuscleTech Mass-Tech Extreme 2000",
    "desc": "Mass gainer with 80g protein and 400g carbs per serving for extreme gains.",
    "price": "250 ₾ (7 lbs)",
    "image": "https://th.bing.com/th/id/OIP.ncaNrROZsWk-g_H-pUppXAHaHa?w=197&h=197&c=7&r=0&o=5&dpr=1.3&pid=1.7"
  },
  {
    "name": "Applied Nutrition Critical Whey",
    "desc": "Blend of whey protein concentrate, isolate, and hydrolysate providing 21g protein per serving.",
    "price": "160 ₾ (2.2 lbs) / 280 ₾ (5.5 lbs)",
    "image": "https://th.bing.com/th/id/OIP.l8FfwH0IsJgbm_u_r2MB0QHaIo?w=155&h=182&c=7&r=0&o=5&dpr=1.3&pid=1.7"
  },
  {
    "name": "Applied Nutrition ABE Pre-Workout",
    "desc": "Pre-workout with 200mg caffeine, 4g citrulline, and 3.25g creatine for performance.",
    "price": "130 ₾ (30 servings)",
    "image": "https://tse2.mm.bing.net/th/id/OIP.tD6gb6q8nkHA_7vyRvBqbAHaHa?rs=1&pid=ImgDetMain"
  },
  {
    "name": "Applied Nutrition ISO-XP",
    "desc": "Zero sugar, zero fat whey protein isolate with 25g protein per serving.",
    "price": "180 ₾ (2 lbs) / 320 ₾ (4 lbs)",
    "image": "https://th.bing.com/th/id/OIP._Fnq-1B7tvO64skXjoGFkAHaHa?w=194&h=193&c=7&r=0&o=5&dpr=1.3&pid=1.7"
  },
  {
    "name": "Applied Nutrition Vegan-Pro",
    "desc": "Plant-based protein blend with 25g protein per serving from soy, pea, and brown rice.",
    "price": "170 ₾ (2.2 lbs)",
    "image": "https://th.bing.com/th/id/OIP.bZRIonjYPBDOB1hXau2iWwHaIt?w=187&h=220&c=7&r=0&o=5&dpr=1.3&pid=1.7"
  },
  {
    "name": "Rule 1 R1 Gain",
    "desc": "Mass gainer with 50g protein and 75g carbs per serving for muscle growth.",
    "price": "220 ₾ (6 lbs)",
    "image": "https://th.bing.com/th/id/OIP.vi8378hlPcLTa4mLEmS1bAHaHa?w=186&h=186&c=7&r=0&o=5&dpr=1.3&pid=1.7"
  },
  {
    "name": "Rule 1 R1 BCAAs",
    "desc": "5g BCAAs in a 2:1:1 ratio to support muscle recovery and endurance.",
    "price": "100 ₾ (30 servings)",
    "image": "https://th.bing.com/th/id/OIP.RExKNN8Bk8FHkGPM73aIRgHaHa?w=183&h=183&c=7&r=0&o=5&dpr=1.3&pid=1.7"
  },
  {
    "name": "Vital Proteins Collagen Peptides",
    "desc": "Collagen peptides to support skin, hair, nails, and joint health. Made with grass-fed, pasture-raised bovine collagen.",
    "price": "130 ₾ (30 servings)",
    "image": "data:image/jpeg;base64,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"
},
{
    "name": "Transparent Labs Bulk Pre-Workout",
    "desc": "Pre-workout designed to boost energy, strength, and endurance with 19 active ingredients like citrulline and beta-alanine. No artificial sweeteners.",
    "price": "160 ₾ (30 servings)",
    "image": "https://th.bing.com/th/id/OIP.6lHkv6TWPkj-vhWABuM0jQHaHa?w=189&h=189&c=7&r=0&o=5&dpr=1.3&pid=1.7"
}



]



@app.route('/vitamins')
def vitamins():
    vitamin_products = [
    {
        "name": "NOW Vitamin C-1000",
        "desc": "Antioxidant protection and immune support",
        "price": "₾37.67",
        "image": "https://th.bing.com/th/id/OIP.nEBPwpFda2csTzx7k385NQHaHa?w=200&h=200&c=7&r=0&o=5&dpr=1.3&pid=1.7"
    },
    {
        "name": "Nature Made Magnesium 250mg",
        "desc": "Supports muscle relaxation and nerve health",
        "price": "₾31.02",
        "image": "https://th.bing.com/th/id/OIP.QDQXY-G2cSMWLIxbMH1j8AHaHa?w=179&h=180&c=7&r=0&o=5&dpr=1.3&pid=1.7"
    },
    {
        "name": "Optimum Nutrition Opti-Men",
        "desc": "Daily multivitamin for men",
        "price": "₾67.47",
        "image": "https://th.bing.com/th/id/OIP.fcNz3vP23AJKPa2Tnt4DCQHaJQ?w=154&h=193&c=7&r=0&o=5&dpr=1.3&pid=1.7"
    },
    {
        "name": "Kirkland Signature Calcium 600mg + D3",
        "desc": "Bone strength support with vitamin D3",
        "price": "₾29.67",
        "image": "https://th.bing.com/th/id/OIP.TRfsE6-YlbnC2jpcDoR8MQHaHa?w=184&h=184&c=7&r=0&o=5&dpr=1.3&pid=1.7"
    },
    {
        "name": "Nature’s Bounty Zinc 50mg",
        "desc": "Supports immune health and skin function",
        "price": "₾21.57",
        "image": "https://th.bing.com/th/id/OIP.We0WhHK2QACSW2bpyWHtigHaHa?w=196&h=196&c=7&r=0&o=5&dpr=1.3&pid=1.7"
    },
    {
        "name": "MegaFood Blood Builder",
        "desc": "Iron supplement with beet root and vitamin C",
        "price": "₾75.47",
        "image": "https://th.bing.com/th/id/OIP.D52WY7RYwYS2x3HM0Ap_bgHaHa?w=197&h=197&c=7&r=0&o=5&dpr=1.3&pid=1.7"
    },
    {
        "name": "One A Day Men’s Multivitamin",
        "desc": "Complete multivitamin with key nutrients",
        "price": "₾40.47",
        "image": "https://th.bing.com/th/id/OIP.dUnz2wUgopbDTYxZeP0uKQHaHa?w=209&h=209&c=7&r=0&o=5&dpr=1.3&pid=1.7"
    },
    {
        "name": "Centrum Silver Adults 50+",
        "desc": "Multivitamin for adults over 50",
        "price": "₾48.47",
        "image": "https://th.bing.com/th/id/OIP.RdCewaFk7wcd2abuo4H9jwHaHa?w=200&h=200&c=7&r=0&o=5&dpr=1.3&pid=1.7"
    },
    {
        "name": "Solgar Vitamin D3 1000 IU",
        "desc": "Supports bone and immune system health",
        "price": "₾25.65", 
        "image": "https://th.bing.com/th/id/OIP.gxXar8WOpr2HtBrdKYM7mwHaHa?w=182&h=182&c=7&r=0&o=5&dpr=1.3&pid=1.7"
    },
    {
        "name": "Nature's Way Alive! Men's Energy",
        "desc": "High potency multivitamin for daily energy",
        "price": "₾53.87", 
        "image": "https://th.bing.com/th/id/OIP.uLsRkojQf4_l39hUp8ZV3AHaHa?w=195&h=195&c=7&r=0&o=5&dpr=1.3&pid=1.7"
    }
]


    return render_template('vitamins.html', vitamins=vitamin_products)




clothes = [
  {
    "name": "Gymshark Onyx T-Shirt",
    "desc": "Premium quality Onyx T-shirt from Gymshark, perfect for workouts.",
    "price": "₾120",
    "image": "https://i.ebayimg.com/thumbs/images/g/l5EAAeSwUuhoHLoI/s-l500.jpg"
  },
  {
    "name": "Gymshark Onyx Joggers",
    "desc": "Comfortable and stylish Onyx joggers for all-day wear.",
    "price": "₾150",
    "image": "https://tse2.mm.bing.net/th/id/OIP.8cB1McNEGNH86aV6-3bjTAHaI1?pid=ImgDet&w=184&h=219&c=7&dpr=1.3"
  },
  {
    "name": "Gymshark Onyx Hoodie",
    "desc": "A soft and cozy Onyx hoodie for every workout.",
    "price": "₾180",
    "image": "https://th.bing.com/th/id/OIP.oC6VfwjkdJElp_gt39Y0TQHaHa?w=208&h=208&c=7&r=0&o=5&dpr=1.3&pid=1.7"
  },
  {
    "name": "Gymshark Legacy Shorts",
    "desc": "Lightweight and breathable Legacy shorts for intense workouts.",
    "price": "₾100",
    "image": "https://th.bing.com/th/id/OIP.Qz_SrSt6BqfSus3VDiuS2QHaI1?w=153&h=183&c=7&r=0&o=5&dpr=1.3&pid=1.7"
  },
  {
    "name": "Youngla Slim Fit Gym Tee",
    "desc": "Youngla’s slim-fit gym tee designed for both style and performance.",
    "price": "₾130",
    "image": "https://th.bing.com/th/id/R.33f76918e696b4c67e3cd97600cacf86?rik=CjhGkUbaX8okRQ&riu=http%3a%2f%2fwww.youngla.com%2fcdn%2fshop%2fproducts%2fYLATrenTwinsD3-14-57.jpg%3fv%3d1678817949&ehk=e1uawlKmvIemNGfurtOifFmnlF56YXTs6yA01EzRUEo%3d&risl=&pid=ImgRaw&r=0"
  },
  {
    "name": "Youngla Performance Joggers",
    "desc": "High-performance joggers by Youngla, perfect for training.",
    "price": "₾140",
    "image": "https://di2ponv0v5otw.cloudfront.net/posts/2022/09/27/6333b07556b2f82acc9ab63d/m_6333b082fed51f6d271e9970.jpg"
  },
  {
    "name": "Youngla Essentials Hoodie",
    "desc": "A must-have hoodie for every gym enthusiast.",
    "price": "₾160",
    "image": "https://th.bing.com/th/id/OIP.nfiDlhidOb162MZqUoSufgHaLG?w=118&h=180&c=7&r=0&o=5&dpr=1.3&pid=1.7"
  },
  {
    "name": "Youngla Gym Tank",
    "desc": "A tank top for your toughest gym sessions, with perfect fit and comfort.",
    "price": "₾110",
    "image": "https://di2ponv0v5otw.cloudfront.net/posts/2023/02/18/63f1b54db635f8b758393847/m_63f1b56abd06290d345bb8c2.jpg"
  },
  {
    "name": "Gymshark Flex Leggings",
    "desc": "Women's flex leggings, providing maximum flexibility.",
    "price": "₾130",
    "image": "https://cdn.shopify.com/s/files/1/0156/6146/files/FLEXHIGHWAISTEDLEGGINGS-Navy-DenimBlue-B1A2Q-UCFX-1602_3ed7acf2-bd26-4f49-8cbe-69168c2075ba_1664x.jpg?v=1690107793"
  },
  {
    "name": "Gymshark Training Jacket",
    "desc": "A lightweight, breathable training jacket for warm-ups.",
    "price": "₾170",
    "image": "https://tse4.mm.bing.net/th/id/OIP.JKe8FfvT1c4LTqVjv2BtBQHaI1?rs=1&pid=ImgDetMain"
  },
  {
    "name": "Gymshark Camo Shorts",
    "desc": "Camo-style workout shorts with a great fit and comfort.",
    "price": "₾90",
    "image": "https://th.bing.com/th/id/OIP.H3RGIzsh4AQZAL9mlgyI1QHaHa?w=219&h=219&c=7&r=0&o=5&dpr=1.3&pid=1.7"
  },
  {
    "name": "Youngla Workout Shorts",
    "desc": "Durable workout shorts for ultimate performance in the gym.",
    "price": "₾100",
    "image": "https://media-photos.depop.com/b1/35144615/1672197455_881d1a8cc529472e9b1cafbb15cf904a/P0.jpg"
  },
  {
    "name": "Youngla Sleeveless Gym Shirt",
    "desc": "Stay cool with this sleeveless gym shirt from Youngla.",
    "price": "₾95",
    "image": "https://media-photos.depop.com/b1/35792549/1579581779_4e5abe477b4242088fd58883bac7f2f6/P0.jpg"
  },
  {
    "name": "Gymshark Performance T-Shirt",
    "desc": "Performance-focused Gymshark T-shirt for all your workouts.",
    "price": "₾115",
    "image": "https://th.bing.com/th/id/R.188a07c8cd01fe59a9459bab6edb516d?rik=J1MM%2bq6WyEpLMw&riu=http%3a%2f%2fcdn.shopify.com%2fs%2ffiles%2f1%2f0185%2f2846%2f9056%2ffiles%2fPowerT-Shirt-GSNavy-A4A9Q-UB9P-0480.jpg%3fv%3d1690386674&ehk=8G2Qa4CMuyAFN2kAh5Qg1jFBgDLhQZN6Ugz6UAZB%2fOs%3d&risl=&pid=ImgRaw&r=0"
  },
  {
    "name": "Youngla Athletic Tank",
    "desc": "Youngla’s athletic tank, designed for heavy lifting and intense cardio.",
    "price": "₾85",
    "image": "https://tse2.mm.bing.net/th/id/OIP.U1z2gkr1EEK_100hSMJJzAHaLG?w=1659&h=2488&rs=1&pid=ImgDetMain"
  }
]























model_name = "distilgpt2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)
model.eval()

def calculate_macros(height, weight, age, gender, activity, goal):
    if gender == "male":
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161

    activity_levels = {
        "low": 1.2,
        "medium": 1.55,
        "high": 1.75,
    }

    tdee = bmr * activity_levels.get(activity, 1.2)

    if goal == "cut":
        tdee -= 500
    elif goal == "bulk":
        tdee += 300

    protein = weight * 2.2
    fats = weight * 1
    carbs = (tdee - (protein * 4 + fats * 9)) / 4

    return {
        "calories": int(tdee),
        "protein": int(protein),
        "fats": int(fats),
        "carbs": int(carbs)
    }




@app.route("/fitness-calculator", methods=["GET", "POST"])
def fitness_calculator():
    macros = None
    

    if request.method == "POST":

        height = int(request.form["height"])
        weight = int(request.form["weight"])
        age = int(request.form["age"])
        gender = request.form["gender"]
        activity = request.form["activity"]
        goal = request.form["goal"]

        macros = calculate_macros(height, weight, age, gender, activity, goal)
            


    return render_template("fitness_calculator.html", macros=macros)
















@app.route('/supplement/<int:id>')
def supplement_detail(id):
    product = next((p for p in clothes if p['id'] == id), None)
    if not product:
        return "Product not found", 404
    return render_template("product_detail.html", product=product)


special_deals = [
    {
        "id": 1,
        "name": "Dymatize ISO100 (Birthday Cake Flavor)",
        "desc": "Limited edition flavor with 25g hydrolyzed protein isolate.",
        "price": "Will Be Given For FREE To Random Buyer",
        "image": "https://tse3.mm.bing.net/th/id/OIP.mlil6bhsQLhQXeQHBdDS_AAAAA?rs=1&pid=ImgDetMain"
    },
    {
        "id": 2,
        "name": "Ghost Legend Pre-Workout",
        "desc": "Energy, focus, and pump – now with 15% discount!",
        "price": "Will Be Given For FREE To Random Buyer",
        "image": "https://th.bing.com/th/id/OIP.x4hb3WWICiaycVRF7KkPDgHaE8?w=276&h=184&c=7&r=0&o=5&dpr=1.3&pid=1.7"
    },
    {
        "id": 3,
        "name": "Optimum Nutrition Serious Mass",
        "desc": "High-calorie weight gainer with 50g protein, 250g carbs and vitamins per serving.",
        "price": "Will Be Given For FREE To Random Buyer",
        "image": "https://th.bing.com/th/id/OIP.3d5XbDAlWM4c2ojy7GxETgHaFp?w=229&h=180&c=7&r=0&o=5&dpr=1.3&pid=1.7"
    },
    {
        "id": 4,
        "name": "RC Pre-Workout",
        "desc": "Explosive energy formula with L-citrulline, beta-alanine, and natural caffeine.",
        "price": "Will Be Given For FREE To Random Buyer ",
        "image": "https://tse2.mm.bing.net/th/id/OIP.wioY_Ha2kB4xfbmS8tpBAwHaHa?rs=1&pid=ImgDetMain"
    }
]



def get_eligible_deals(cart_total):
    eligible = []
    for deal in special_deals:
        threshold = int(deal["price"].split("₾")[1].strip().replace("₾", "").replace(" ", ""))
        if cart_total >= threshold:
            eligible.append(deal)
    return eligible







@app.route('/supplement-benefits')
def supplement_benefits():
    return render_template('supplement-benefits.html')


@app.route('/payments')
def payments():
    return render_template('payments.html')





@app.route('/', methods=['GET', 'POST'])
def index():
    query = request.args.get('q', '')  # Get search query from the request

    filtered_products = products

    if query:
        # Filter products by the query
        filtered_products = [
            product for product in products
            if query.lower() in product['name'].lower() or query.lower() in product['desc'].lower()
        ]

    return render_template('index.html', products=filtered_products, clothes=clothes,special_deals=special_deals)

@app.route('/clothes', methods=['GET'])
def clothes_section():
    search_query = request.args.get('q')  # Get the search query from the form
    filtered_clothes = clothes  # Default to showing all clothes

    if search_query:
        # Filter clothes by the search query
        filtered_clothes = [product for product in clothes if search_query.lower() in product['name'].lower()]

    return render_template("clothes.html", clothes=filtered_clothes)




@app.route('/add-to-cart', methods=['POST'])
def add_to_cart():
    name = request.form.get('product_name')
    price = request.form.get('product_price')
    image = request.form.get('product_image')

    if not name or not price:
        flash('Missing product info')
        return redirect(url_for('home'))

    item = {'name': name, 'price': price.strip(), 'image': image}

    if 'cart' not in session:
        session['cart'] = []

    session['cart'].append(item)
    session.modified = True

    return redirect(url_for('cart'))






@app.route('/cart')
def cart():
    cart = session.get('cart', [])
    total = 0

    for item in cart:
        price_str = item['price']

        
        try:
            # Use regex to find the first number in the string
            import re
            match = re.search(r'(\d+(\.\d+)?)', price_str)
            if match:
                price = float(match.group(1))
                total += price
        except:
            continue  # skip if price can't be parsed

    return render_template('cart.html', cart=cart, total=total)




@app.route('/product/<int:product_id>')
def view_product(product_id):
    if product_id >= 0 and product_id < len(products):
        product = products[product_id]
        return render_template('product_detail.html', product=product)
    else:
        return "Product not found", 404


@app.route('/checkout')
def checkout():
    if 'user' not in session:
        flash('Please log in to proceed to checkout.')
        return redirect(url_for('login'))
    
    cart = session.get('cart', [])
    if not cart:
        flash('Your cart is empty.')
        return redirect(url_for('cart'))

    total = 0
    for item in cart:
        price = item['price']
        try:
            if "₾" in price:
                price_val = float(price.split("₾")[0].strip())
            elif "GEL" in price:
                price_val = float(price.split("GEL")[0].strip())
            else:
                price_val = float(price.strip())
        except (ValueError, AttributeError):
            price_val = 0.0  # fallback if price is empty or malformed

        total += price_val

    return render_template("checkout.html", cart=cart, total=total)




@app.route('/claim-free-gift', methods=['POST'])
def claim_free_gift():
    gift_id = int(request.form.get('free_gift_id'))
    gift = next((d for d in special_deals if d['id'] == gift_id), None)
    
    if gift:
        cart = session.get("cart", [])
        cart.append({
            "name": gift["name"] + " (Free Gift)",
            "price": "0 ₾",
            "image": gift["image"]
        })
        session["cart"] = cart
    
    return redirect("/checkout")




@app.route('/order-summary', methods=['POST'])
def order_summary():
    cart = session.get('cart', [])
    total = 0
    for item in cart:
        price_part = item['price'].split('₾')[0].strip()
        total += float(price_part)

    name = request.form['name']
    address = request.form['address']
    phone = request.form['phone']

    return render_template('order_summary.html', cart=cart, total=total, name=name, address=address, phone=phone)

@app.route('/remove-from-cart', methods=['POST'])
def remove_from_cart():
    product_name = request.form['product_name']

   
    if 'cart' in session:
        cart_items = session['cart']
        session['cart'] = [item for item in cart_items if item['name'] != product_name]
        session.modified = True  

    return redirect('/cart')

@app.route('/thank-you', methods=['POST'])
def thank_you():
    session.pop('cart', None)  
    return render_template('thank_you.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users:
            flash('Username already exists. Please choose a different username.')
            return redirect(url_for('signup'))  
        else:
            users[username] = password
            flash('Signup successful! Please login.')
            return redirect(url_for('login'))  
    return render_template('signup.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users and users[username] == password:
            session['user'] = username
            flash('Login successful!')
            return redirect(url_for('index'))  
        else:
            flash('Invalid username or password.')
            return redirect(url_for('login'))  
    return render_template('login.html')




@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Logged out successfully.')
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
