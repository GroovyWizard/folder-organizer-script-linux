#!/bin/bash
declare -a book_cache=()
should_run_book=false
counter=-1


mount_cache() {
	while IFS= read -r file; do
		book_cache+=("$file")
	done  < <(find $BOOKS_PATH -type f -name "*.epub" -o -name "*.pdf")
}


is_integer() {
    local arg="$1"
    if [[ $arg =~ ^[0-9]+$ ]]; then
        return 0  
    else
        return 1 
    fi
}


select_book() {
	local book_id="$1"
	local cache_size="${#book_cache[@]}"
	local index=book_id
		

	if (( index >= 0 && index < cache_size )); then 
		local element="${book_cache[index]}"
		echo "$element"
	else 
		echo "Invalid book ID"
		return 1
	fi

}


open_with_book_reader() {
	if [ -z "$arg_r" ]; then
	  echo "Invalid argument for -r option"
	  return 1
	fi

	if is_integer "$arg_r"; then
	    echo "$arg_r is an integer."
	else
	    echo "$arg_r is not an integer."
	    return 1
	fi

	echo "Opening with default reader in path $BOOK_READER"
	book_path=$(select_book "$arg_r")

	if [[ $? -eq 1 ]]; then
	    echo "Error occurred."
	    return 1
	fi

	echo $book_path
	nohup zathura -l -debug "$book_path" &
	return 0
}

list_books() {
	for book in "${book_cache[@]}"; do
		((counter++))
		echo "Id:($counter) Path: $book"
	done
}


mount_cache
while getopts ":lr:" opt; do
  case ${opt} in
    l )
      echo "--- Listing books in $BOOKS_PATH directory ---"
      list_books
      ;;
    r )
      arg_r="$OPTARG"
      open_with_book_reader
      ;;
    \? )
      echo "Invalid option: $OPTARG"
      ;;
    : )
      echo "Option -$OPTARG requires an argument"
      ;;
  esac
done
shift $((OPTIND -1))


