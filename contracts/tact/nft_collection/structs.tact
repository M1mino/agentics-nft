struct CollectionData {
    next_item_index: Int;
    collection_content: Cell;
    owner_address: Address;
}

struct RoyaltyParams {
    numerator: Int;
    denominator: Int;
    destination: Address;
}

struct RarityInfo {
    tier: Int as uint8;  // 0=Common, 1=Rare, 2=Epic, 3=Legendary
}
