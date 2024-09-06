 mongorestore --uri="$MONGODB_URI" \
    --nsFrom="sample_mflix.embedded_movies" \
    --nsTo="${first_last}.movies_${first_last}" \
    --nsInclude="sample_mflix.embedded_movies" \
    "dump_without_vectors/dump/"