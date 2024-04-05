import io
import time

import requests
from bs4 import BeautifulSoup


URL = "https://www.bbr.com/bbx/search/listed"


def main():
    start = time.time()
    page = 0
    headers = {}
    writer = io.StringIO()
    writer.write(
        "wine_name,case_format,note,availability,price_per_case,reviewer,rating\n"
    )
    try:
        while True:
            print(f"Page: {page + 1}")
            request_body = {
                "q": ":bbr-vintage-asc:inStockFlag:true:approvalStatus:APPROVED",
                "page": page,
                "sort": "bbr-vintage-desc",
                "pageSize": "60",
                "ajax": True
            }
            res = requests.get(URL, headers=headers, params=request_body)
            html = res.text
            soup = BeautifulSoup(html, "html.parser")
            prod_list = soup.css.select("div.prod_list")
            if len(prod_list) == 0:
                break

            for product in prod_list:
                wine_name = product.css.select("div.productInBondTitle")[0].get_text().strip()
                try:
                    reviewer = product.css.select("span.expertReview")[0].get_text().strip()
                except:
                    reviewer = ""
                try:
                    rating = product.css.select("span.expertReviewRating")[0].get_text().strip()
                except:
                    rating = ""

                for info in product.css.select("div.inbondVariantInfo"):
                    case_format = info.css.select("span.caseSize")[0].get_text().strip().replace("\xa0", " ")
                    availability = info.css.select("span.availableCases")[0].get_text().strip()
                    price_per_case = info.css.select("span.variantPrice")[0].get_text().strip()
                    note = info.css.select("span.variantLabel")[0].get_text().strip()
                    writer.write(
                        f'"{wine_name}","{case_format}","{note}","{availability}",'
                        f'"{price_per_case}","{reviewer}","{rating}"\n'
                    )
            page += 1
    except Exception as exc:
        print(f"Error: {exc}")
        raise

    with open("./bbr_output.csv", "w", encoding="utf-8") as f:
        f.write(writer.getvalue())

    writer.close()

    print(f"Done!. {round(time.time() - start, 2)}s")


if __name__ == '__main__':
    main()
