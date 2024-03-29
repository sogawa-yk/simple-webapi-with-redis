DECLARE
    -- データ生成の回数を指定
    total_records NUMBER := 1000000;
BEGIN
    FOR i IN 1..total_records LOOP
        INSERT INTO products (product_name, price, stock_quantity)
        VALUES (
            'Product ' || TO_CHAR(i),
            DBMS_RANDOM.VALUE(100, 1000), -- 100から1000の間でランダムな価格
            DBMS_RANDOM.VALUE(10, 1000)  -- 10から1000の間でランダムな在庫数
        );
        
        -- 10000件ごとにコミットする（必要に応じて調整）
        IF MOD(i, 10000) = 0 THEN
            COMMIT;
        END IF;
    END LOOP;
    COMMIT; -- 残りのデータをコミット
END;
/

