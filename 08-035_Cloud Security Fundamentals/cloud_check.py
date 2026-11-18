# cloud_check.py

# Simulated cloud inventory data
buckets = [
    {
        "name": "customer-data",
        "public": True,
        "encrypted": False
    },
    {
        "name": "internal-logs",
        "public": False,
        "encrypted": True
    }
]

iam_roles = [
    {
        "name": "ReadOnlyAnalytics",
        "policies": ["s3:GetObject", "s3:ListBucket"]
    },
    {
        "name": "OverPoweredAdmin",
        "policies": ["*:*"]
    }
]


def check_buckets(buckets):
    """
    Checks storage buckets for public exposure and lack of encryption.
    """
    print("\n--- Storage Bucket Security Audit ---")
    for bucket in buckets:
        name = bucket["name"]
        is_public = bucket.get("public", False)
        is_encrypted = bucket.get("encrypted", False)
        
        # Collect detected issues and recommended fixes for this bucket
        issues = []
        fixes = []
        
        # Check 1: Ensure bucket is not exposed to the public internet
        if is_public:
            issues.append("Bucket is publicly accessible to the internet")
            fixes.append("disable public access")
            
        # Check 2: Verify that encryption at rest is enabled
        if not is_encrypted:
            issues.append("Data is not encrypted at rest")
            fixes.append("enable server-side encryption")
            
        # Print audit findings based on evaluation
        if issues:
            print(f"[ALERT] Resource: {name}")
            print(f"  Issue: {', and '.join(issues)}.")
            print(f"  Fix: Please {' and '.join(fixes)}.\n")
        else:
            print(f"[OK] Resource: {name} passes security checks.\n")


def check_iam_roles(iam_roles):
    """
    Checks IAM roles for wildcard (*:*) policies violating least privilege.
    """
    print("--- IAM Role Security Audit ---")
    for role in iam_roles:
        name = role["name"]
        policies = role.get("policies", [])
        
        # Check if full admin access (*:*) was granted instead of scoped permissions
        has_wildcard = "*:*" in policies
        
        if has_wildcard:
            print(f"[ALERT] Resource: {name}")
            print("  Issue: Overly permissive policy '*:*' detected (violates Principle of Least Privilege).")
            print("  Fix: Restrict policy actions to only the specific services and resource ARNs required.\n")
        else:
            print(f"[OK] Resource: {name} adheres to standard permission policies.\n")


def main():
    # Run audit and display summary report
    print("========================================")
    print("   CLOUD CONFIGURATION AUDIT REPORT     ")
    print("========================================")
    check_buckets(buckets)
    check_iam_roles(iam_roles)
    print("Audit completed.")


# Execute audit report when run directly
if __name__ == "__main__":
    main()