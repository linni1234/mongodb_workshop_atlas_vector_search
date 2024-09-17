mongoimport --uri="$MONGODB_URI" \
    --collection="routes_${first_last}" \
    --db="${first_last}" \
    --file="routes.json" \
    --jsonArray