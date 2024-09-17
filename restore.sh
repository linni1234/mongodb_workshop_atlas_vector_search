mongoimport --uri="$MONGODB_URI" \
    --collection="movies_${first_last}" \
    --db="${first_last}" \
    --file="movies_with_embedding.json" \
    --jsonArray