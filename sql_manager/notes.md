## SQL Connection Notes

| **Field** | **Relation**              | **Data Type** | **Example** |
|-----------|---------------------------|---------------|-------------|
| stockref  | The EAN Number            | varchar(45)   | 5200        |
| datetime  | Time of Update            | datetime      | ...         |
| price     | RRP Price of Item         | double        | 5.39        |
| source    | Assuming source of price? | varchar(15)   | Bestway?    |
| vat       | The VAT of Item (0/20)?   | double        | 0.2 or 20?  |

- Only need to access these values; matching based on title seems nonferrous as names are not matched.
- Match values based off **EAN VALUE**.
- ID; if value not present, append new item and increase ID by 1 of MAX>

### **Ask about VAT AND SOURCE.**