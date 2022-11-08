for i in {1..10}; do
    {
	    curl 'http://10.109.232.51:8080/function/bert-squad.faas-share-fn/?question=What%20food%20does%20Harry%20like?&&context=My%20name%20is%20Harry%20and%20I%20grew%20up%20in%20Canada.%20I%20love%20bananas.'
    } 
done
