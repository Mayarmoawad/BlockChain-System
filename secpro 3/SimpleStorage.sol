pragma solidity >=0.6.0 <0.9.0;

contract SimpleStorage {
    bytes hashed_Data;
    bytes previous_hash;

    function store(bytes memory hashed_Data_, bytes memory previous_hash_)
        public
    {
        hashed_Data = hashed_Data_;
        previous_hash = previous_hash_;
    }

    
}
