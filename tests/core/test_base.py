from ...core.base import BaseService

service =  BaseService()

table = service.execute_query("""
SELECT
    season,
    constructor_name,
    standing
FROM formula1.gold.v_constructors_standing
WHERE constructor_name = 'Ferrari'
  AND standing = 1
ORDER BY season;
""")



print(table)
