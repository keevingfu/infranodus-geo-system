#!/usr/bin/env python3
"""
Quick test script to verify Docker service connections
"""

import sys

# Test Neo4j connection
print("Testing Neo4j connection...")
try:
    from neo4j import GraphDatabase

    driver = GraphDatabase.driver(
        "neo4j://localhost:7689",
        auth=("neo4j", "geo_password_2025")
    )

    with driver.session() as session:
        result = session.run("RETURN 'Hello from Neo4j!' as message")
        record = result.single()
        print(f"✅ Neo4j: {record['message']}")

        # Get version
        result = session.run("CALL dbms.components() YIELD name, versions RETURN name, versions[0] as version")
        for record in result:
            print(f"   Version: {record['name']} {record['version']}")

    driver.close()
except Exception as e:
    print(f"❌ Neo4j connection failed: {e}")
    sys.exit(1)

# Test Redis connection
print("\nTesting Redis connection...")
try:
    import redis

    r = redis.Redis(
        host='localhost',
        port=6380,
        password='redis_password',
        decode_responses=True
    )

    # Test basic operations
    r.set('test_key', 'Hello from Redis!')
    value = r.get('test_key')
    print(f"✅ Redis: {value}")

    # Get info
    info = r.info('server')
    print(f"   Version: Redis {info['redis_version']}")

    # Cleanup
    r.delete('test_key')
except Exception as e:
    print(f"❌ Redis connection failed: {e}")
    sys.exit(1)

print("\n🎉 All Docker services are working correctly!")
print("\nService URLs:")
print("  Neo4j Browser: http://localhost:7476")
print("  Neo4j Bolt: neo4j://localhost:7689")
print("  Redis: localhost:6380")
