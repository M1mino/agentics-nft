message(0x693d3950) GetRoyaltyParams {
    query_id: Int as uint64;
}

message(0xa8cb00ad) ReportRoyaltyParams {
    query_id: Int as uint64;
    numerator:  Int as uint16;
    denominator: Int as uint16;
    destination: Address;
}

message SetMintPrice {
    query_id: Int as uint64;
    new_price: Int as coins;
}