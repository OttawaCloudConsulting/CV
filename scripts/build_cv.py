#!/usr/bin/env python3
"""
build_cv.py — CV as Code build pipeline.

Renders CV.md from:
  - assets/projects/project_*.json (project data)
  - data/personal.json (personal info, certifications, executive summary)
  - templates/cv.md.j2 (Jinja2 template)

Usage:
    python3 scripts/build_cv.py [--output PATH] [--template PATH]

Adding a new role:
    1. Copy assets/projects/project_template.json to project_N.json
    2. Fill in all fields including date_range
    3. Add sub-project files as project_N.M.json
    4. Run this script
"""

import json
import math
import re
import argparse
from collections import defaultdict
from pathlib import Path

try:
    from jinja2 import Environment, FileSystemLoader, select_autoescape
except ImportError:
    print("Error: jinja2 is not installed. Run: pip install jinja2")
    raise SystemExit(1)

REPO_ROOT = Path(__file__).parent.parent
PROJECTS_DIR = REPO_ROOT / "assets" / "projects"
PERSONAL_FILE = REPO_ROOT / "data" / "personal.json"
TEMPLATES_DIR = REPO_ROOT / "templates"
DEFAULT_OUTPUT = REPO_ROOT / "CV.md"
DEFAULT_TEMPLATE = "cv.md.j2"
TECH_INDEX_OUTPUT = REPO_ROOT / "TECHNOLOGY_INDEX.md"
TECH_INDEX_TEMPLATE = "tech_index.md.j2"


def load_personal():
    with open(PERSONAL_FILE) as f:
        return json.load(f)


def load_projects():
    """Load all project JSON files, excluding template."""
    projects = []
    for path in sorted(PROJECTS_DIR.glob("project_*.json")):
        if path.name == "project_template.json":
            continue
        with open(path) as f:
            data = json.load(f)
        projects.append(data["project"])
    return projects


def is_parent(number):
    """Return True if the project number is an integer (parent role)."""
    return number == math.floor(number)


def number_to_str(number):
    """Format a project number for display: 13 -> '13', 13.1 -> '13.1'."""
    if is_parent(number):
        return str(int(number))
    # Format decimal numbers cleanly
    s = f"{number:.1f}"
    # Handle cases like 2.10 -> still 2.1
    return s.rstrip("0").rstrip(".")


def parse_month_year(date_str):
    """Parse 'Month YYYY' to a sortable tuple (year, month_idx)."""
    month_order = {
        "january": 1, "february": 2, "march": 3, "april": 4,
        "may": 5, "june": 6, "july": 7, "august": 8,
        "september": 9, "october": 10, "november": 11, "december": 12,
    }
    parts = date_str.strip().split()
    if parts[0].lower() == "current":
        return (9999, 12)
    try:
        month = month_order.get(parts[0].lower(), 0)
        year = int(parts[1]) if len(parts) > 1 else 0
        return (year, month)
    except (IndexError, ValueError):
        return (0, 0)


def build_project_groups(projects):
    """
    Separate projects into parents and sub-projects.
    Group sub-projects under their parent.
    For orphan sub-projects (no parent file), synthesise a parent.
    Returns a list of group dicts sorted by number descending.
    """
    parents = {}
    sub_projects = defaultdict(list)

    for p in projects:
        num = p["number"]
        if is_parent(num):
            parents[int(num)] = p
        else:
            parent_num = int(math.floor(num))
            sub_projects[parent_num].append(p)

    # Sort sub-projects within each group by number ascending
    for parent_num in sub_projects:
        sub_projects[parent_num].sort(key=lambda p: p["number"])

    # Build all group numbers (union of parent keys and sub-project parent keys)
    all_parent_nums = sorted(
        set(parents.keys()) | set(sub_projects.keys()), reverse=True
    )

    groups = []
    for n in all_parent_nums:
        subs = sub_projects.get(n, [])
        if n in parents:
            group = dict(parents[n])
            group["_number_int"] = n
            group["_number_str"] = str(n)
            group["sub_projects"] = subs
        else:
            # Synthesise parent from sub-project data
            first_sub = subs[0]
            # Compute combined date range across all subs
            starts = [parse_month_year(s["date_range"]["start"]) for s in subs]
            ends = [parse_month_year(s["date_range"]["end"]) for s in subs]
            earliest_start = min(starts, key=lambda x: x)
            latest_end = max(ends, key=lambda x: x)
            # Find original string values corresponding to min/max
            start_str = subs[starts.index(earliest_start)]["date_range"]["start"]
            if latest_end == (9999, 12):
                end_str = "Current"
            else:
                end_str = subs[ends.index(latest_end)]["date_range"]["end"]

            group = {
                "number": n,
                "title": first_sub.get("title", f"Project {n}"),
                "client": first_sub.get("client", {}),
                "role": first_sub.get("role", ""),
                "date_range": {"start": start_str, "end": end_str},
                "challenge": None,
                "solution": None,
                "outcomes": [],
                "technologies": [],
                "_number_int": n,
                "_number_str": str(n),
                "_synthesised": True,
                "sub_projects": subs,
            }

        # Assemble role_overview deliverables and outcomes from sub-project parentsummary
        if subs and "role_overview" in group:
            group["role_overview"] = dict(group["role_overview"])  # don't mutate original
            group["role_overview"]["deliverables"] = [
                s["parentsummary"]["deliverables"]
                for s in subs
                if s.get("parentsummary", {}).get("deliverables")
            ]
            group["role_overview"]["outcomes"] = [
                s["parentsummary"]["outcomes"]
                for s in subs
                if s.get("parentsummary", {}).get("outcomes")
            ]

        groups.append(group)

    return groups


TECH_GROUPS_ORDER = [
    "Amazon Web Services",
    "Microsoft Azure",
    "Kubernetes & Containers",
    "Infrastructure as Code",
    "CI/CD & DevOps",
    "Security Tooling",
    "Compliance Frameworks",
    "Identity & Access Management",
    "Observability & Monitoring",
    "Networking",
    "Languages & Scripting",
    "Databases & Storage",
    "Messaging & Eventing",
    "Application Servers & Middleware",
    "Operating Systems & Virtualization",
    "Microsoft 365 & Collaboration",
    "Legacy & On-Premises",
    "Uncategorised",
]

TECH_GROUP_MAP = {
    # Amazon Web Services
    "Amazon AWS": "Amazon Web Services",
    "Amazon AWS (AWS CDK v1/v2, AWS CodeCommit, AWS CodePipeline, AWS CodeBuild, AWS CodeDeploy, AWS Cloud9, AWS Glue, AWS DMS, AWS Lambda)": "Amazon Web Services",
    "Amazon AWS (AWS Organizations, AWS Control Tower, AWS SSO, AWS Config, AWS CloudTrail, AWS GuardDuty, AWS IAM, AWS CodePipeline, AWS CodeBuild, AWS CodeDeploy, AWS CloudFormation, Terraform)": "Amazon Web Services",
    "Amazon AWS Cloud": "Amazon Web Services",
    "Amazon AWS Organizations": "Amazon Web Services",
    "Amazon AWS US": "Amazon Web Services",
    "API Gateway": "Amazon Web Services",
    "AWS ALB (Load Balancer)": "Amazon Web Services",
    "AWS Auto-Scaling": "Amazon Web Services",
    "AWS CDK": "Infrastructure as Code",
    "AWS CDK v1.x": "Infrastructure as Code",
    "AWS CDK v2.x": "Infrastructure as Code",
    "AWS Certificate Manager": "Amazon Web Services",
    "AWS CloudFormation": "Infrastructure as Code",
    "AWS CloudFront": "Amazon Web Services",
    "AWS CloudTrail": "Amazon Web Services",
    "AWS CloudWatch": "Observability & Monitoring",
    "AWS CodeBuild": "CI/CD & DevOps",
    "AWS CodePipeline": "CI/CD & DevOps",
    "AWS Config": "Amazon Web Services",
    "AWS Control Tower": "Amazon Web Services",
    "AWS EBS Storage": "Amazon Web Services",
    "AWS EC2": "Amazon Web Services",
    "AWS ECR": "Amazon Web Services",
    "AWS ECS": "Amazon Web Services",
    "AWS EFS": "Amazon Web Services",
    "AWS ELB (Load Balancer)": "Amazon Web Services",
    "AWS GuardDuty": "Amazon Web Services",
    "AWS IAM": "Identity & Access Management",
    "AWS Inspector": "Amazon Web Services",
    "AWS Lambda": "Amazon Web Services",
    "AWS Linux": "Operating Systems & Virtualization",
    "AWS Managed SSO": "Identity & Access Management",
    "AWS Organizations": "Amazon Web Services",
    "AWS Parameter Store": "Amazon Web Services",
    "AWS RDS": "Databases & Storage",
    "AWS Route 53": "Networking",
    "AWS S3": "Databases & Storage",
    "AWS Secrets Store": "Amazon Web Services",
    "AWS Service Catalog": "Amazon Web Services",
    "AWS Service Discovery": "Amazon Web Services",
    "AWS SES": "Messaging & Eventing",
    "AWS SSO": "Identity & Access Management",
    "AWS Systems Manager": "Amazon Web Services",
    "AWS Transfer Service (SFTP)": "Amazon Web Services",
    "AWS Transit Gateway": "Networking",
    "AWS Transit Peering": "Networking",
    "AWS Trusted Advisor": "Observability & Monitoring",
    "AWS VPC": "Networking",
    "AWS VPN": "Networking",
    "AWS WAF & Shield": "Security Tooling",
    "AWS X-Ray": "Observability & Monitoring",
    "CDK": "Infrastructure as Code",
    "CloudFormation": "Infrastructure as Code",
    "CloudWatch": "Observability & Monitoring",
    "EventBridge": "Messaging & Eventing",
    "Load Balancers": "Networking",
    "Service Control Policies": "Amazon Web Services",
    "SNS": "Messaging & Eventing",
    "SQS": "Messaging & Eventing",
    "Step Functions": "Messaging & Eventing",
    "Transit Gateway": "Networking",
    # Amazon EKS — Kubernetes
    "Amazon EKS": "Kubernetes & Containers",
    "IRSA": "Kubernetes & Containers",
    # Microsoft Azure
    "Azure Active Directory": "Identity & Access Management",
    "Azure Application Gateways": "Microsoft Azure",
    "Azure Availability Sets": "Microsoft Azure",
    "Azure CLI": "Languages & Scripting",
    "Azure DevOps": "CI/CD & DevOps",
    "Azure DevOps Git": "CI/CD & DevOps",
    "Azure DevOps Pipelines": "CI/CD & DevOps",
    "Azure Images": "Microsoft Azure",
    "Azure Load Balancers": "Microsoft Azure",
    "Azure Network Security Groups": "Microsoft Azure",
    "Azure PostgreSQL Database": "Databases & Storage",
    "Azure PowerShell": "Languages & Scripting",
    "Azure Resource Groups": "Microsoft Azure",
    "Azure Resource Manager (ARM)": "Infrastructure as Code",
    "Azure Sentinel": "Security Tooling",
    "Azure Storage Accounts": "Databases & Storage",
    "Azure Virtual Machine Scale Sets": "Microsoft Azure",
    "Azure Virtual Machines": "Microsoft Azure",
    "Azure Virtual Networks": "Microsoft Azure",
    "Microsoft Azure": "Microsoft Azure",
    # Kubernetes & Containers
    "Argo Workflows": "Kubernetes & Containers",
    "ArgoCD": "Kubernetes & Containers",
    "CDK8s": "Kubernetes & Containers",
    "Cilium": "Kubernetes & Containers",
    "Crossplane": "Kubernetes & Containers",
    "Docker": "Kubernetes & Containers",
    "Docker Containers": "Kubernetes & Containers",
    "Docker Images": "Kubernetes & Containers",
    "Helm": "Kubernetes & Containers",
    "Helm Charts": "Kubernetes & Containers",
    "Kubernetes": "Kubernetes & Containers",
    "Kubernetes (kind, k3d, kubeadm)": "Kubernetes & Containers",
    "OCI Bundles": "Kubernetes & Containers",
    # Infrastructure as Code
    "KCL": "Infrastructure as Code",
    "Terraform": "Infrastructure as Code",
    "Terraform 0.12.7": "Infrastructure as Code",
    "YAML": "Infrastructure as Code",
    "JSON": "Infrastructure as Code",
    # CI/CD & DevOps
    "Atlassian Confluence": "CI/CD & DevOps",
    "Atlassian Jira": "CI/CD & DevOps",
    "Atlassian JIRA": "CI/CD & DevOps",
    "Confluence": "CI/CD & DevOps",
    "Git": "CI/CD & DevOps",
    "GitHub": "CI/CD & DevOps",
    "GitLab": "CI/CD & DevOps",
    "HipChat": "CI/CD & DevOps",
    "JFROG Artifactory": "CI/CD & DevOps",
    "Jenkins": "CI/CD & DevOps",
    "JIRA": "CI/CD & DevOps",
    # Security Tooling
    "Checkov Security Scanning": "Security Tooling",
    "Checkov Security Scanning (BridgeCrew/Prisma)": "Security Tooling",
    "CIS Hardened Images": "Security Tooling",
    "Cloudflare WAF": "Security Tooling",
    "Code & IaC Security Scanning": "Security Tooling",
    "LUKS Encryption": "Security Tooling",
    "SIEM": "Security Tooling",
    "SonarQube & Dependency Checker": "Security Tooling",
    "SSL/TLS": "Security Tooling",
    "TerraScan Security Scanning (Tenable)": "Security Tooling",
    "WatchGuard (next-gen firewall)": "Security Tooling",
    # Compliance Frameworks
    "CIS Controls": "Compliance Frameworks",
    "FISMA": "Compliance Frameworks",
    "HIPAA": "Compliance Frameworks",
    "ISO:27001": "Compliance Frameworks",
    "Microsoft Office 365 Compliance": "Compliance Frameworks",
    "NERC": "Compliance Frameworks",
    "NIST": "Compliance Frameworks",
    "NIST Frameworks": "Compliance Frameworks",
    "PCI-DSS 3.0": "Compliance Frameworks",
    "PIPEDA": "Compliance Frameworks",
    "US DOD NOFORN": "Compliance Frameworks",
    # Identity & Access Management
    "Active Directory": "Identity & Access Management",
    "Microsoft Active Directory": "Identity & Access Management",
    "Microsoft Intune": "Identity & Access Management",
    "OpenLDAP": "Identity & Access Management",
    "RBAC": "Identity & Access Management",
    # Observability & Monitoring
    "Elasticsearch": "Observability & Monitoring",
    "Grafana": "Observability & Monitoring",
    "ManageEngine Desktop Central": "Observability & Monitoring",
    "Prometheus": "Observability & Monitoring",
    "SNMP": "Observability & Monitoring",
    # Networking
    "CloudFlare CDN": "Networking",
    "Cloudflare DNS": "Networking",
    "Cross-Region Networking": "Networking",
    "Hybrid Cloud": "Networking",
    "Layer 3 Switching": "Networking",
    "VLAN": "Networking",
    # Languages & Scripting
    "Bash": "Languages & Scripting",
    "Golang": "Languages & Scripting",
    "Java": "Languages & Scripting",
    "Java 8.x": "Languages & Scripting",
    "PHP": "Languages & Scripting",
    "PowerShell": "Languages & Scripting",
    "Python": "Languages & Scripting",
    "Python 3.x": "Languages & Scripting",
    "SQL": "Languages & Scripting",
    "Typescript": "Languages & Scripting",
    # Databases & Storage
    "IBM FC SAN": "Databases & Storage",
    "IBM SAN": "Databases & Storage",
    "NexentaStor": "Databases & Storage",
    "PostgreSQL": "Databases & Storage",
    # Messaging & Eventing
    "Kafka": "Messaging & Eventing",
    # Application Servers & Middleware
    "Apache": "Application Servers & Middleware",
    "IBM WebSphere": "Application Servers & Middleware",
    "NGINX": "Application Servers & Middleware",
    "SOGO": "Application Servers & Middleware",
    "Tomcat": "Application Servers & Middleware",
    "Tomcat 8.x": "Application Servers & Middleware",
    "WSO2": "Application Servers & Middleware",
    # Operating Systems & Virtualization
    "CentOS": "Operating Systems & Virtualization",
    "CentOS 6/7": "Operating Systems & Virtualization",
    "CentOS 7": "Operating Systems & Virtualization",
    "CentOS 7.x": "Operating Systems & Virtualization",
    "Citrix Desktop Streaming": "Operating Systems & Virtualization",
    "Citrix XenServer": "Operating Systems & Virtualization",
    "Microsoft Hyper-V": "Operating Systems & Virtualization",
    "Microsoft Windows 2016": "Operating Systems & Virtualization",
    "Microsoft Windows 2019": "Operating Systems & Virtualization",
    "VMware": "Operating Systems & Virtualization",
    "VMware 5.0": "Operating Systems & Virtualization",
    "VMWare 6": "Operating Systems & Virtualization",
    "VMware ESXi 6": "Operating Systems & Virtualization",
    "Windows 2012 R2": "Operating Systems & Virtualization",
    "Windows Server 2008 R2": "Operating Systems & Virtualization",
    "Windows Server 2012 R2 RDS": "Operating Systems & Virtualization",
    # Microsoft 365 & Collaboration
    "Cisco CUCM": "Microsoft 365 & Collaboration",
    "Exchange Online": "Microsoft 365 & Collaboration",
    "ITIL ServiceDesk": "Microsoft 365 & Collaboration",
    "Lotus Domino 9": "Microsoft 365 & Collaboration",
    "Microsoft Exchange": "Microsoft 365 & Collaboration",
    "Microsoft Exchange 2010": "Microsoft 365 & Collaboration",
    "Microsoft Office 365": "Microsoft 365 & Collaboration",
    "Microsoft Skype for Business": "Microsoft 365 & Collaboration",
    "Office 365": "Microsoft 365 & Collaboration",
    "SharePoint 2016": "Microsoft 365 & Collaboration",
    "Xerox XMPie": "Microsoft 365 & Collaboration",
    # Legacy & On-Premises
    "ADP": "Legacy & On-Premises",
    "ADP PIN Pads": "Legacy & On-Premises",
    "GE Fanuc": "Legacy & On-Premises",
    "IBM AS/400": "Legacy & On-Premises",
    "IBM Cluster": "Legacy & On-Premises",
    "Info BPCS": "Legacy & On-Premises",
    "Lawson Movex (M3)": "Legacy & On-Premises",
    "Ottawa Tier 2 Data Centre": "Legacy & On-Premises",
    "POS": "Legacy & On-Premises",
    "RackSpace": "Legacy & On-Premises",
    "RackSpace Sydney": "Legacy & On-Premises",
    "Rogers Data Centre": "Legacy & On-Premises",
    "SCADA": "Legacy & On-Premises",
    "Thin Client": "Legacy & On-Premises",
    "Tier II Data Centre": "Legacy & On-Premises",
    "Tier III Data Centre": "Legacy & On-Premises",
}


def _resolve_tech_group(tech_name):
    """Resolve a technology name to a group using the map, then prefix fallback."""
    if tech_name in TECH_GROUP_MAP:
        return TECH_GROUP_MAP[tech_name]
    if tech_name.startswith("AWS ") or tech_name.startswith("Amazon "):
        return "Amazon Web Services"
    if tech_name.startswith("Azure ") or tech_name.startswith("Microsoft Azure"):
        return "Microsoft Azure"
    return "Uncategorised"


def build_grouped_tech_index(groups):
    """
    Auto-aggregate technology items grouped by domain category.
    Returns an ordered dict of group_name -> list of (tech_item, [project_refs]).
    """
    tech_map = defaultdict(set)  # tech_item -> set of project number strings

    def collect(project, num_str):
        for tech_group in project.get("technologies", []):
            for item in tech_group.get("items", []):
                tech_map[item].add(num_str)

    for group in groups:
        parent_num_str = group["_number_str"]
        if group.get("technologies"):
            collect(group, parent_num_str)
        for sub in group.get("sub_projects", []):
            sub_num_str = number_to_str(sub["number"])
            collect(sub, sub_num_str)

    # Assign each tech to a group
    grouped = defaultdict(list)
    for tech, proj_nums in sorted(tech_map.items(), key=lambda x: x[0].upper()):
        category = _resolve_tech_group(tech)
        sorted_nums = sorted(proj_nums, key=lambda x: float(x))
        grouped[category].append((tech, sorted_nums))

    # Return in defined order, skipping empty groups
    result = {}
    for group_name in TECH_GROUPS_ORDER:
        if group_name in grouped:
            result[group_name] = grouped[group_name]
    return result


def build_tech_index(groups):
    """
    Auto-aggregate technology items from all projects into an alphabetical index.
    Returns an OrderedDict of letter -> list of (tech_item, [project_refs]).
    """
    tech_map = defaultdict(set)  # tech_item -> set of project number strings

    def collect(project, num_str):
        for tech_group in project.get("technologies", []):
            for item in tech_group.get("items", []):
                tech_map[item].add(num_str)

    for group in groups:
        parent_num_str = group["_number_str"]
        # Collect from parent (if it has technologies, e.g. standalone parent)
        if group.get("technologies"):
            collect(group, parent_num_str)
        # Collect from sub-projects
        for sub in group.get("sub_projects", []):
            sub_num_str = number_to_str(sub["number"])
            collect(sub, sub_num_str)

    # Sort by tech name, group by first letter
    index = defaultdict(list)
    for tech, proj_nums in sorted(tech_map.items(), key=lambda x: x[0].upper()):
        letter = tech[0].upper()
        sorted_nums = sorted(proj_nums, key=lambda x: float(x))
        index[letter].append((tech, sorted_nums))

    # Sort letters
    return dict(sorted(index.items()))


def render(output_path=None, template_name=DEFAULT_TEMPLATE):
    personal_data = load_personal()
    projects = load_projects()
    groups = build_project_groups(projects)
    tech_index = build_tech_index(groups)
    grouped_tech_index = build_grouped_tech_index(groups)

    def make_anchor(heading):
        """Generate a GitHub-flavored Markdown anchor from a heading string."""
        s = heading.lower()
        # Remove characters that aren't alphanumeric, spaces, or hyphens
        s = re.sub(r"[^\w\s-]", "", s)
        # Replace spaces with hyphens
        s = re.sub(r"\s+", "-", s.strip())
        return s

    def project_refs(num_set):
        """Format a set of project number strings into 'Project N' or 'Projects N, M'."""
        nums = sorted(num_set, key=lambda x: float(x))
        if len(nums) == 1:
            return f"Project {nums[0]}"
        return "Projects " + ", ".join(nums)

    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        autoescape=select_autoescape([]),
        keep_trailing_newline=True,
        trim_blocks=True,
        lstrip_blocks=True,
    )
    env.filters["anchor"] = make_anchor

    template = env.get_template(template_name)

    output = template.render(
        personal=personal_data["personal"],
        profile=personal_data["professional_profile"],
        executive=personal_data["executive_summary"],
        groups=groups,
        tech_index=tech_index,
        number_to_str=number_to_str,
        project_refs=project_refs,
    )

    out_path = Path(output_path) if output_path else DEFAULT_OUTPUT
    out_path.write_text(output, encoding="utf-8")
    print(f"Generated: {out_path}")
    print(f"  Projects: {sum(1 for g in groups for _ in ([g] if not g.get('sub_projects') else g['sub_projects']))} entries across {len(groups)} roles")

    # Render Technology Index as a separate file
    tech_template = env.get_template(TECH_INDEX_TEMPLATE)
    tech_output = tech_template.render(tech_index=tech_index, grouped_tech_index=grouped_tech_index)
    TECH_INDEX_OUTPUT.write_text(tech_output, encoding="utf-8")
    print(f"Generated: {TECH_INDEX_OUTPUT}")


def main():
    parser = argparse.ArgumentParser(description="Build CV.md from project JSON files")
    parser.add_argument("--output", help="Output path (default: CV.md)", default=None)
    parser.add_argument("--template", help="Template name (default: cv.md.j2)", default=DEFAULT_TEMPLATE)
    args = parser.parse_args()
    render(output_path=args.output, template_name=args.template)


if __name__ == "__main__":
    main()
