#!/usr/bin/env python3
"""Build cv_data.json from CV.md content using the schema skeleton structure."""
import json

data = {
    "personal": {
        "name": "Mr. Christian Turner",
        "title": "Senior Cloud Architect & DevSecOps Specialist",
        "tagline": "Comprehensive Technical CV & Project Portfolio",
        "subtitle": "Detailed technical expertise documentation and project history",
        "email": "CTurner@OttawaCloudConsulting.com",
        "phone": "+1 (613) 796-3300",
        "location": {
            "city": "Ottawa",
            "province": "Ontario",
            "country": "Canada"
        },
        "links": {
            "linkedin": "linkedin.com/in/Christian-Turner-CloudPro",
            "github": "github.com/OttawaCloudConsulting"
        },
        "consulting_entity": "Ottawa Cloud Consulting Inc."
    },
    "professional_profile": {
        "summary": [
            "Mr. Turner is a Senior Cloud Architect and DevSecOps Specialist with 15+ years of AWS-focused platform engineering experience, including nine consecutive years delivering cloud solutions to Canadian Federal Government clients. He has achieved Authority to Operate (ATO) status on multiple government AWS environments, led enterprise-scale Kubernetes and GitOps platform implementations at Shared Services Canada, and holds four active AWS certifications including Solutions Architect \u2013 Professional. His engagements span SSC, Agriculture Canada, and the Department of National Defence, with consistent delivery against ITSG-22/33/38, NIST 800-53, and Government of Canada cloud guardrail requirements.",
            "Mr. Turner operates through Ottawa Cloud Consulting Inc., a federally incorporated consulting practice, delivering cloud architecture, DevSecOps, infrastructure automation, and compliance-driven platform engineering. His expertise spans AWS-native development, multi-account governance, containerized workloads (EKS, Kubernetes), GitOps pipelines (ArgoCD, Azure DevOps), and IaC at enterprise scale (Terraform, CDK, CloudFormation).",
            "His experience includes successful cloud migrations across healthcare, utilities, and political sector clients with HIPAA, NIST, and ITSG compliance requirements. As a Subject Matter Expert, he engages directly with technical teams, management, and executive stakeholders to deliver architecture that is secure, automated, and auditable."
        ],
        "language": "English",
        "certifications": [
            {"name": "AWS Certified SysOps Administrator - Associate", "issuer": "Amazon Web Services", "certificate_url": "./assets/certificates/AWS Certified SysOps Administrator - Associate.pdf"},
            {"name": "AWS Certified Solutions Architect - Associate", "issuer": "Amazon Web Services", "certificate_url": "./assets/certificates/AWS Certified Solutions Architect - Associate.pdf"},
            {"name": "AWS Certified Solutions Architect - Professional", "issuer": "Amazon Web Services", "certificate_url": "./assets/certificates/AWS Certified Solutions Architect - Professional.pdf"},
            {"name": "AWS Certified Developer - Associate", "issuer": "Amazon Web Services", "certificate_url": "./assets/certificates/AWS Certified Developer - Associate.pdf"},
            {"name": "Certified Scrum Master (CSM - Scrum Alliance)", "issuer": "Scrum Alliance", "certificate_url": "./assets/certificates/Scrum Alliance - Certified ScrumMaster.pdf"}
        ]
    },
    "executive_summary": {
        "specialization": "AWS Cloud Architecture, DevSecOps, and Platform Engineering for Canadian Federal Government and regulated sector clients",
        "government_clients": "Shared Services Canada (SSC), Agriculture Canada, Department of National Defence (DND) \u2014 9+ consecutive years",
        "compliance_depth": "ITSG-22/33/38, NIST 800-53, Government of Canada Cloud Guardrails, HIPAA; multiple Authority to Operate (ATO) achievements",
        "cloud_platforms": "AWS (primary, 15+ years), Microsoft Azure, Google Cloud",
        "current_engagement": "Cloud Platform Engineering, Shared Services Canada \u2014 September 2023 to Present",
        "certifications": "AWS Solutions Architect \u2013 Professional, AWS Solutions Architect \u2013 Associate, AWS SysOps Administrator \u2013 Associate, AWS Developer \u2013 Associate, Certified ScrumMaster (CSM)",
        "consulting_entity": "Ottawa Cloud Consulting (federally incorporated) \u2014 Principal Consultant",
        "availability": "2-week notice period"
    },
    "projects": [],
    "technology_index": []
}

# Helper to make task objects
def t(task, sub_tasks=None):
    return {"task": task, "sub_tasks": sub_tasks or []}

def te(category, items):
    return {"category": category, "items": items}

# ============================================================
# PROJECT 13
# ============================================================
p13 = {
    "number": 13,
    "title": "SSC - Cloud Platform Engineering / Hosting Services Branch",
    "client": {"name": "Shared Services Canada", "department": "Hosting Services Branch", "team": "Cloud Platform Engineering"},
    "role": "AWS Cloud Infrastructure as Code DevOps Engineer & Architect",
    "date_range": {"start": "September 2023", "end": "Current"},
    "description": "",
    "outcomes": [],
    "technical_environment": [],
    "sub_projects": [
        {
            "number": "13.1",
            "title": "Cloud Services Directorate, Cloud Platform Engineering",
            "date_range": {"start": "September 2023", "end": "Current"},
            "description": "The Cloud Services Platform Engineering team operates within the Hosting Services Branch providing an Enterprise class Tenancy within the Amazon Web Services (AWS) Cloud, supporting AWS ASEA (Secure Accelerator) and AWS LZA (Landing Zone Accelerator) platform designs.",
            "outcomes": "Successfully architected and deployed enterprise-class GitOps platform serving multiple government departments through AWS EKS and ArgoCD. Established Infrastructure as Code standards using Terraform and Crossplane, enabling rapid deployment of NIST 800-53 compliant workloads across SSC's AWS Landing Zone Accelerator platform.",
            "tasks_performed": [
                t("Needs analysis, defining requirements, defining and maintain deliverable scopes"),
                t("AWS and Kubernetes design patterns and architecture"),
                t("Design and Delivery Iterations", ["Concept > Proof of Concept (PoC) > Dev/Test > Minimal Viable Product (MVP) > Production > Continuous Improvements"]),
                t("Infrastructure as Code development", ["Terraform", "Crossplane", "Kubernetes"]),
                t("Deployment Processes and Implementations", ["GitOps declarative (ArgoCD)", "Pipeline Promotions (Terraform)", "ClickOps and Runbooks"]),
                t("Security By Design patterns and principles", ["Meet and exceed NIST 800-53 & ITSG", "General Security Best Practices", "Code Security (Vulnerability and Quality)"]),
                t("Workload and Application Deployment and Support", ["Deployment Processes", "Implementation", "Architectural Patterns"]),
                t("Implemented Source Code Management, DevOps Toolings, and DevOps Best Practices")
            ],
            "technical_environment": [
                te("Public Cloud", ["Amazon AWS Cloud", "Azure DevOps"]),
                te("Applications", ["Azure DevOps Git", "ArgoCD", "Argo Workflows", "Checkov Security Scanning", "JIRA", "Confluence"]),
                te("Servers", ["Kubernetes (kind, k3d, kubeadm)", "AWS Linux", "CentOS", "CIS Hardened Images"]),
                te("Languages", ["Bash", "Python 3.x", "Typescript", "Golang", "Terraform", "Crossplane", "Helm", "CDK", "CDK8s"])
            ]
        },
        {
            "number": "13.2",
            "title": "Cloud Services Directorate, Automation and Orchestration Framework",
            "date_range": {"start": "September 2023", "end": "Current"},
            "description": "The Cloud Services Directorate requires comprehensive automation and orchestration frameworks to support enterprise-scale cloud deployments across multiple government departments and regulated sectors. This initiative focuses on developing scalable, compliant, and secure cloud automation solutions through Ottawa Cloud Consulting's federally incorporated consulting services.",
            "outcomes": "Architected 3 multi-account AWS organizations managing 200+ workloads with governance, SCPs, identity models, and compliance baselines aligned to NIST, CIS, and ITSG. Improved deployment frequency by 30% through GitOps automation with ArgoCD and Azure DevOps, managing over 50 microservices. Designed 30+ serverless, event-driven, and containerized workloads reducing operational overhead by 40% and infrastructure costs by $25K annually. Engineered 3 production EKS clusters achieving 99.9% uptime while reducing Kubernetes onboarding time by over 60% through deterministic automation and developer Golden Paths.",
            "tasks_performed": [
                t("Needs analysis, architecture design, and implementation of multi-account AWS organizations"),
                t("Design and implementation of Service Control Policies (SCPs) and governance frameworks"),
                t("Identity and Access Management (IAM) model architecture with compliance baselines"),
                t("GitOps automation framework development and implementation", ["ArgoCD deployment and configuration management", "Azure DevOps integration and pipeline orchestration", "Microservice deployment automation for 50+ services"]),
                t("Serverless and event-driven architecture design and implementation", ["AWS Lambda, Step Functions, EventBridge, SQS, SNS", "Container orchestration with AWS EKS and Docker", "Cost optimization strategies achieving $25K annual savings"]),
                t("Production EKS cluster engineering and management", ["3 node groups with auto-scaling configurations", "IRSA (IAM Roles for Service Accounts) implementation", "Multi-node isolation and security hardening", "Cilium networking configuration and management", "RBAC model design and implementation", "99.9% uptime achievement through high availability design"]),
                t("Crossplane and KCL provisioning framework development", ["Modular infrastructure component design", "Versioned OCI bundle creation and management", "100+ infrastructure component provisioning automation", "75% reduction in deployment errors through standardization"]),
                t("Developer experience optimization and Golden Path creation", ["Kubernetes onboarding automation reducing time by 60%", "Deterministic automation workflow development", "Self-service deployment capabilities"]),
                t("Observability and monitoring implementation", ["12 operational dashboards covering metrics, security, compliance, logs", "Incident response signal integration", "Multi-organization monitoring across 3 AWS accounts"]),
                t("Documentation and knowledge management", ["25+ design specifications and architecture documents", "ConOps (Concept of Operations) development", "Runbooks and operational procedures", "Security models and compliance frameworks"]),
                t("Compliance and security framework alignment", ["NIST, CIS, and ITSG compliance baseline implementation", "Automated security scanning and governance", "Regulatory compliance reporting and monitoring"])
            ],
            "technical_environment": [
                te("Public Cloud", ["Amazon AWS Organizations", "AWS Control Tower", "AWS SSO", "AWS Config", "AWS CloudTrail", "AWS GuardDuty"]),
                te("Container Orchestration", ["Amazon EKS", "Docker", "Kubernetes", "Helm"]),
                te("GitOps & CI/CD", ["ArgoCD", "Argo Workflows", "Azure DevOps", "Git"]),
                te("Infrastructure as Code", ["Crossplane", "KCL", "Terraform", "AWS CDK", "CloudFormation"]),
                te("Serverless & Event-Driven", ["AWS Lambda", "Step Functions", "EventBridge", "SQS", "SNS", "API Gateway"]),
                te("Networking", ["Cilium", "AWS VPC", "Transit Gateway", "Load Balancers"]),
                te("Security & Compliance", ["AWS IAM", "IRSA", "RBAC", "Service Control Policies", "CIS Controls", "NIST Frameworks"]),
                te("Observability", ["CloudWatch", "Prometheus", "Grafana", "AWS X-Ray", "ElasticSearch"]),
                te("Languages", ["Python", "Golang", "Typescript", "Bash", "YAML", "JSON", "KCL"]),
                te("Package Management", ["OCI Bundles", "Helm Charts", "Docker Images"])
            ]
        }
    ]
}
data["projects"].append(p13)

# ============================================================
# PROJECT 12
# ============================================================
p12 = {
    "number": 12,
    "title": "Agriculture Canada - Cloud Centre of Expertise / Cloud Operations",
    "client": {"name": "Agriculture Canada", "department": "Cloud Centre of Expertise", "team": "Cloud Operations"},
    "role": "AWS Cloud DevOps Architect (Part-Time)",
    "date_range": {"start": "January 2021", "end": "September 2023"},
    "description": "",
    "outcomes": [],
    "technical_environment": [],
    "sub_projects": [
        {
            "number": "12.1",
            "title": "Cloud Centre of Expertise / Cloud Operations",
            "date_range": {"start": "January 2021", "end": "September 2023"},
            "description": "The AAFC Cloud Centre of Expertise (CCoE) are focused on providing a secure and scalable managed public cloud environment to internal business users. The AWS Cloud environment is implemented using standard AWS Landing Zone foundations with layers of Infrastructure as Code governance resources deployed to meet both Operational and Security requirements, as well as achieve full ATO status for production workloads.",
            "outcomes": "Achieved full ATO (Authority to Operate) status for Agriculture Canada's AWS Cloud environment, meeting ITSG-22/33/38 requirements. Successfully implemented automated security and governance compliance tooling that exceeded GoC cloud guardrails, enabling secure cloud adoption across the department with integrated Azure AD SSO federation.",
            "tasks_performed": [
                t("Needs analysis, define requirements, and strategize architecture with AWS team"),
                t("Architectural design and Proof of Concept (PoC) implementation for design review sessions"),
                t("Infrastructure as Code (IaC) Coding and review", ["AWS CLI, AWS API", "Infrastructure As Code (IAC) - Terraform, AWS SDK, AWS CLI Scripting"]),
                t("CI/CD CodePipeline, Azure DevOps Repos, Azure Pipelines/AWS CodeBuild, CodeDeploy"),
                t("Implementation of IT Security Program to meet ITSG-22, ITSG-33 and ITSG-38 and TBS driven cloud guardrails and achieve Full ATO"),
                t("Secure, implement and support SSO Federation to Azure Active Directory"),
                t("Develop and implement Security Control Systems and Posture Management to manage integration of AWS Cloud Identity components, validating against ITSG Controls"),
                t("Design and integration of automated Security and Governance compliance tooling, meeting and exceeding GoC ITSG requirements"),
                t("Facilitated requirements gathering with technical team, architecture team, and security team"),
                t("Support client workloads", ["Needs analysis and POC discussions", "Architecture and Design", "Review, Governance and Compliance", "Technological challenges", "Implementation and Infrastructure Coding"]),
                t("Source Code Management within Azure DevOps (Git) Repos"),
                t("DevOps integration with DevOps tooling, methodology, and processes", ["Drive Git and Infrastructure Development strategies", "Drive Event Driven Architecture design", "Drive Data Driven Infrastructure Coding"]),
                t("Documentation, Knowledge transfer and cross-training with team, new staff and onboarded clients")
            ],
            "technical_environment": [
                te("Public Cloud", ["Amazon AWS (AWS Organizations, AWS Control Tower, AWS SSO, AWS Config, AWS CloudTrail, AWS GuardDuty, AWS IAM, AWS CodePipeline, AWS CodeBuild, AWS CodeDeploy, AWS CloudFormation, Terraform)"]),
                te("Public Cloud (Azure)", ["Azure DevOps", "Azure Active Directory", "Azure Sentinel"]),
                te("Applications", ["Microsoft Active Directory", "Bash", "Azure DevOps Git", "Azure DevOps Pipelines", "CloudFormation", "Checkov Security Scanning (BridgeCrew/Prisma)", "TerraScan Security Scanning (Tenable)"]),
                te("Servers", ["Microsoft Windows 2019", "AWS Linux", "CentOS", "CIS Hardened Images"])
            ]
        },
        {
            "number": "12.2",
            "title": "DevOps & AWS Development",
            "date_range": {"start": "January 2021", "end": "September 2023"},
            "description": "The Analytics team is focused on designing, developing and deploying applications for data analysis that operate in the AWS Cloud to meet departmental analytical requirements provided data.",
            "outcomes": "Delivered critical analytics platform supporting analytics operations through AWS cloud-native architecture for client workload systems. Implemented comprehensive DevSecOps pipeline with automated security scanning and supply chain management, enabling secure data analysis capabilities.",
            "tasks_performed": [
                t("Needs analysis, define requirements, and strategize architecture with AWS team"),
                t("Architectural design and Proof of Concept (PoC) implementation for design review sessions"),
                t("Infrastructure as Code (IaC) Coding and review", ["AWS CLI, AWS API", "Infrastructure As Code (IAC) - AWS CDK, AWS SDK, AWS CLI Scripting"]),
                t("CI/CD Pipelines - AWS CodeCommit, AWS CodePipeline, AWS CodeBuild, AWS CodeDeploy"),
                t("Implementation and maintenance of CI/CD AWS Resources meeting best practices and agile deployment"),
                t("Security and Governance reporting on Code and IaC to support DevSecOps compliance"),
                t("Continuous improvement of Deployment Practices and Release Management", ["Source Code Control - GIT & AWS CodeCommit", "Development Practices - AWS Cloud9 and integrations for development team", "Code Quality - SonarQube integration and reporting", "Automation - Pipeline automation and continual enhancements", "Security - Code supply chain management (container, python & node packages) using JFROG Artifactory"]),
                t("Developer Tasks", ["Overlapping developer support for AWS Resources and Application Code", "AWS Glue batch job architecture", "AWS DMS (Database Migration Service)", "AWS Serverless architecture", "AWS Event Driven Architecture design and implementation"])
            ],
            "technical_environment": [
                te("Public Cloud", ["Amazon AWS (AWS CDK v1/v2, AWS CodeCommit, AWS CodePipeline, AWS CodeBuild, AWS CodeDeploy, AWS Cloud9, AWS Glue, AWS DMS, AWS Lambda)"]),
                te("Public Cloud (Azure)", ["Azure DevOps"]),
                te("Applications", ["Bash", "Azure DevOps", "Git", "Atlassian Jira", "Code & IaC Security Scanning", "JFROG Artifactory", "SonarQube & Dependency Checker", "AWS CDK v1.x", "AWS CDK v2.x"])
            ]
        }
    ]
}
data["projects"].append(p12)

# ============================================================
# PROJECT 11
# ============================================================
p11 = {
    "number": 11,
    "title": "SSC CSD R&D",
    "client": {"name": "Shared Services Canada", "department": "Cloud Services Directorate", "team": "Cloud Platform Engineering"},
    "role": "AWS Cloud Infrastructure as Code DevOps Engineer & Architect",
    "date_range": {"start": "September 2019", "end": "January 2021"},
    "description": "",
    "outcomes": [],
    "technical_environment": [],
    "sub_projects": [
        {
            "number": "11.1",
            "title": "Cloud Services Directorate, Cloud Platform Engineering Project",
            "date_range": {"start": "September 2019", "end": "January 2021"},
            "description": "The CSD R&D Project group are focused on generating a set of deployable Infrastructure as Code (IaC) for re-use within SSC and partners. Infrastructure as Code (IaC) supports automation of 'CSD Landing Zone' integrating AWS Landing Zone customisation, SAA Security Guard Rails, and generic multi-purpose tools. Developed and drove success and security achievements to ATO with AWS Secure Environment Accelerator.",
            "outcomes": "First team to achieve ATO status using AWS Secure Environment Accelerator (ASEA), establishing reusable Infrastructure as Code templates for government-wide adoption. Created foundational 'CSD Landing Zone' architecture that became the standard for SSC cloud deployments, supporting critical workloads including SCED, DX, and Email systems.",
            "tasks_performed": [
                t("Needs analysis, define requirements, and strategize architecture with AWS team"),
                t("Architectural design and Proof of Concept (PoC) implementation for design review sessions"),
                t("Infrastructure as Code (IaC) Coding", ["AWS CLI, AWS SDK/API", "AWS CloudFormation", "Terraform"]),
                t("CI/CD CodePipeline, CodeCommit, CodeBuild, CodeDeploy"),
                t("GitLab, GitHub"),
                t("Implementation of IT Security Program to meet ITSG-22, ITSG-33 and ITSG-38 and TBS driven cloud guardrails and achieve iATO"),
                t("Design, secure and implementation of SSO Federation with Azure Active Directory"),
                t("Designed and codified the AWS IAM access control framework for the CSD Landing Zone"),
                t("Facilitated requirements gathering with technical team, architecture team, and security team"),
                t("Client Deployment of AWS Native resources to provide governance and generate iATO evidence packages"),
                t("Source Code Management within GitLab"),
                t("DevOps integration with DevOps tooling, methodology, and processes"),
                t("Documentation, Knowledge transfer and cross-training with team, new staff and onboarded clients"),
                t("Achieve ATO status for AWS Cloud"),
                t("Supporting onboarding of workloads (SCED, DX, Vocalls, Email)")
            ],
            "technical_environment": [
                te("Public Cloud", ["Amazon AWS Cloud", "AWS VPC", "AWS CloudFront", "AWS CloudWatch", "AWS CloudTrail", "AWS IAM", "AWS EC2", "AWS ECS", "AWS SES", "AWS S3", "AWS RDS", "AWS CloudFormation", "AWS Service Catalog", "AWS Route 53", "AWS Systems Manager", "AWS Trusted Advisor", "AWS VPN", "AWS ELB (Load Balancer)", "AWS ALB (Load Balancer)", "AWS Transit Gateway", "AWS Transit Peering", "AWS GuardDuty", "AWS WAF & Shield", "AWS Inspector", "AWS Certificate Manager", "AWS Auto-Scaling", "AWS EBS Storage", "AWS Managed SSO", "AWS CodeBuild", "AWS CodePipeline", "AWS Organizations", "AWS Config", "AWS Systems Manager"]),
                te("Applications", ["Microsoft Active Directory", "Bash", "GitLab", "GitHub", "CloudFormation"]),
                te("Servers", ["Microsoft Windows 2019", "AWS Linux"])
            ]
        }
    ]
}
data["projects"].append(p11)

# ============================================================
# PROJECT 10
# ============================================================
p10 = {
    "number": 10,
    "title": "DND DPDCS SMMS Replacement Project",
    "client": {"name": "Department of National Defence", "department": "DPDCS", "team": "SMMS Replacement Project"},
    "role": "Cloud Architect - Resilient Systems",
    "date_range": {"start": "February 2019", "end": "December 2020"},
    "description": "",
    "outcomes": [],
    "technical_environment": [],
    "sub_projects": [
        {
            "number": "10.1",
            "title": "SMMS Search and Rescue Replacement Project",
            "date_range": {"start": "February 2019", "end": "December 2020"},
            "description": "This project will replace the current SARMASTER software and hardware while providing reliable backup Site capability. It will provide interface capability to accept 'live data' and the Geographic Information System (GIS). Lastly, the software will include long term support to ensure continued SAR operational readiness.",
            "outcomes": "Successfully modernized critical Search and Rescue operations system with zero downtime migration to AWS cloud infrastructure. Delivered containerized architecture using Docker/ECS with PostgreSQL, ensuring 24/7 availability for life-saving SAR operations across Canada while meeting stringent DND security requirements.",
            "tasks_performed": [
                t("Project Management using Agile methodologies, and hybrid reporting"),
                t("Needs analysis, define requirements, and strategize high level Cloud Architecture"),
                t("Architectural design and PoC implementation with modernization of infrastructure", ["Docker - ECS Containers & externalisation of data strategy", "AutoScaling - Scale of containers & scale of EC2 instances", "Monitoring - CloudWatch and EventBridge based Event Driven Architecture and response to events", "Application - Java, Tomcat/Apache, PostgreSQL applications"]),
                t("Security Coordination and architectural alignment to required Guidelines (ITSG-33, DND & TSB Cloud Compliance)"),
                t("Implementation of IT Security to meet ITSG controls and achieve iATO"),
                t("Engineered the access control posture for the SAR replacement platform"),
                t("Facilitated requirements gathering with technical and systems team, business team and project management, external stakeholders, and security teams"),
                t("Review and realign infrastructure as required from continuous development cycles"),
                t("Staged implementation testing of services with inline remediation"),
                t("Internal feedback to development and operations for change coordination"),
                t("Integration to CI/CD pipeline, automation, and management systems", ["CI/CD - Git, Jenkins, CodePipeline, CodeCommit, CodeBuild, CodeDeploy"]),
                t("Infrastructure as Code (IaC) deliverables in CloudFormation, deployed as Service Catalog Products"),
                t("Provide final architecture and documentation"),
                t("Pre-migratory testing and security reporting, and failure/high-availability testing"),
                t("Migration and cut-over processes"),
                t("Documentation, knowledge transfer and cross-training with Operations staff, Development staff, and Management")
            ],
            "technical_environment": [
                te("Public Cloud", ["Amazon AWS Cloud", "AWS VPC", "AWS CloudFront", "AWS CloudWatch", "AWS CloudTrail", "AWS IAM", "AWS EC2", "AWS ECS", "AWS ECR", "AWS SES", "AWS S3", "AWS EFS", "AWS RDS", "AWS CloudFormation", "AWS Service Catalog", "AWS Route 53", "AWS Systems Manager", "AWS Trusted Advisor", "AWS VPN", "AWS ELB (Load Balancer)", "AWS ALB (Load Balancer)", "AWS Transit Gateway", "AWS Transit Peering", "AWS GuardDuty", "AWS WAF & Shield", "AWS Inspector", "AWS Certificate Manager", "AWS Auto-Scaling", "AWS EBS Storage", "AWS Service Discovery", "AWS Transfer Service (SFTP)", "AWS Parameter Store", "AWS Secrets Store"]),
                te("Applications", ["PostgreSQL", "Docker Containers", "Bash", "Terraform 0.12.7", "Java 8.x", "Tomcat 8.x", "Atlassian JIRA", "Atlassian Confluence", "WSO2", "Kafka", "PHP", "GIT", "OpenLDAP", "SOGO", "ManageEngine Desktop Central", "CloudFormation"]),
                te("Servers", ["Microsoft Windows 2016", "AWS Linux", "CentOS 7.x"])
            ]
        }
    ]
}
data["projects"].append(p10)

# ============================================================
# PROJECT 9
# ============================================================
p9 = {
    "number": 9,
    "title": "IDS Data Systems (New Democratic Party)",
    "client": {"name": "IDS Data Systems", "department": "", "team": ""},
    "role": "Cloud Architect",
    "date_range": {"start": "November 2018", "end": "January 2019"},
    "description": "This project supplemented the organizations workforce to complete two key cloud migration projects.",
    "outcomes": [
        "Migrated the New Democratic Party of Canada's voice communications infrastructure from Cisco CUCM on-premise telephony to Microsoft Office 365 / Skype for Business at the Ottawa NCR corporate headquarters, delivering with zero voice service interruption.",
        "Migrated bespoke voter data workloads from VMware 6 on-premise to Microsoft Azure, implementing Protected B-equivalent security controls for citizen voting information.",
        "Delivered both engagements within a combined 8-week window under political operational deadline constraints."
    ],
    "technical_environment": [],
    "sub_projects": [
        {
            "number": "9.1",
            "title": "Office 365 Skype Migration - New Democratic Party of Canada",
            "date_range": {"start": "November 2018", "end": "January 2019"},
            "description": "The client was migrating from a traditional distributed on-premise phone system to a fully virtualized Office 365 tenanted system.",
            "outcomes": "",
            "tasks_performed": [
                t("Internal directory configuration reviews"),
                t("Migration planning and aligning to tool requirements", ["Active Directory Design and Management", "Active Directory Federation Services", "Exchange Online + Litigation/Auditing Features", "Exchange Online Security Configuration and access policies", "Microsoft Office Software and deployment strategies", "Microsoft Skype for Business deployment"]),
                t("Deployment of Office365 specific features to support Skype for Business"),
                t("Manage migration settings and deprecation of Cisco CUCM"),
                t("Implementation of IT Security and Cyber Protection to meet required Security Controls for Voice and Unified Communication Systems"),
                t("Facilitated requirements gathering with client technical and support teams, governance and security teams, key user stakeholders, and management"),
                t("Office 365 user configurations"),
                t("Office 365, Skype for Business, and Microsoft Teams Security and Policy writing"),
                t("PowerShell scripting and automation"),
                t("Migration Review and end user documentation"),
                t("Knowledge transfer and cross-training with internal teams and onboarded client")
            ],
            "technical_environment": [
                te("Public Cloud", ["Microsoft Office 365", "Microsoft Skype for Business", "Microsoft Office 365 Compliance", "Azure PowerShell"])
            ]
        },
        {
            "number": "9.2",
            "title": "Server Workload Cloud Migration - New Democratic Party of Canada",
            "date_range": {"start": "November 2018", "end": "January 2019"},
            "description": "The client was migrating a bespoke server workload, comprised of local database, compute functions, and public accessibility into the public cloud from traditional on-premise VMWare 6 infrastructure. The cloud transformation platform selected was Microsoft Azure.",
            "outcomes": "",
            "tasks_performed": [
                t("Project Management using Agile methodologies, and hybrid reporting"),
                t("Needs analysis, define requirements, and strategize high level Cloud Architecture"),
                t("Architectural design and PoC implementation with modernization of infrastructure", ["Azure ARM, Resource Groups", "Virtual Machine, Scale Sets, Availability Sets, Machine Images", "Azure VNET, Load Balancers, Network Security Groups, Application Gateway", "Azure Storage Accounts, Blob Storage, Block Storage", "Azure PostgreSQL Database", "CI/CD Jenkins automation deployment", "Java, Spring Framework, and PostgreSQL application", "ELK and ElasticSearch Application", "Azure CLI, PowerShell and Terraform"]),
                t("Staged implementation testing of services with inline remediation"),
                t("Internal feedback to development vendor and client IT operations for change coordination"),
                t("Implementation of IT Security and Cyber Protection to meet required Security Controls for data system maintaining voting citizen information, equivalent to Protected B data"),
                t("PowerShell and Azure CLI based deployment automation, change management, and smoke tests"),
                t("Provide final architecture and documentation for production blue-green deployment"),
                t("Pre-migratory testing and security reporting, and failure/high-availability testing"),
                t("Knowledge transfer and cross-training with internal teams and support vendor")
            ],
            "technical_environment": [
                te("Public Cloud", ["Microsoft Azure", "Azure Resource Manager (ARM)", "Azure Resource Groups", "Azure Virtual Machines", "Azure Virtual Machine Scale Sets", "Azure Availability Sets", "Azure Images", "Azure Virtual Networks", "Azure Load Balancers", "Azure Network Security Groups", "Azure Application Gateways", "Azure Storage Accounts", "Azure PostgreSQL Database", "Cloudflare DNS", "CloudFlare CDN"]),
                te("Applications", ["Java", "Tomcat", "Apache", "Elasticsearch", "PowerShell", "Azure PowerShell", "Azure CLI"]),
                te("Servers", ["CentOS 6/7", "Windows 2012 R2", "VMWare 6"]),
                te("Security", ["WatchGuard (next-gen firewall)", "Cloudflare WAF"])
            ]
        }
    ]
}
data["projects"].append(p9)

# ============================================================
# PROJECT 8
# ============================================================
p8 = {
    "number": 8,
    "title": "SSC CITS SMG & CTMS",
    "client": {"name": "Shared Services Canada", "department": "CITS - Infrastructure Security", "team": ""},
    "role": "Senior Business / Technical Architect",
    "date_range": {"start": "January 2018", "end": "February 2019"},
    "description": "As a Senior Business and Technical Architect, worked on several projects within the Cyber and Information Technology Security (CITS) Branch at Shared Services Canada. The CITS branch's focus is to protect the Government of Canada's (GC) systems and networks, as well as Canadians' information from cyber threats.",
    "outcomes": [
        "Replaced Excel-based security assessment tracking for SSC's Security Management & Governance teams with a structured SharePoint 2016 platform, standardizing intake, assessment, and milestone tracking workflows across all GC department audit cycles.",
        "Implemented Atlassian JIRA and Confluence for SSC's Cyber Threat Management team, introducing Kanban visualization and Definition of Done standards that improved workload management and reporting visibility for approximately 25 security practitioners.",
        "Deployed LUKS-encrypted, SSL-secured JIRA infrastructure with automated daily backups, meeting SSC's Protected B data handling requirements."
    ],
    "technical_environment": [
        te("Applications", ["SharePoint 2016", "JIRA", "HipChat", "Confluence", "NGINX", "Bash", "PostgreSQL"]),
        te("Servers", ["VMWare ESXI 6", "CentOS 7", "Windows 2012", "GCDOCS", "VMWare"])
    ],
    "sub_projects": [
        {
            "number": "8.1",
            "title": "SharePoint 2016 Design",
            "date_range": {"start": "July 2018", "end": "February 2019"},
            "description": "The client was implementing a SharePoint solution for managing and tracking tasks performed by a number of Security Management and Governance teams. Existing processes relied heavily on Microsoft Excel spreadsheets for reporting, with non-standardized content.",
            "outcomes": "",
            "tasks_performed": [
                t("Review the 'as-is' implementation and align it with the work methodologies and requirements for all SM&G teams"),
                t("Using a simplified business process mapping and gap analysis strategy, created and refined key workflows to track the process from Business Intake, through Security Assessment (SA) process, and completion with milestone tracking and funding recovery tracking"),
                t("Helped to design the system to standardize meta-data types and vernacular, enforcing data integrity and data value"),
                t("Implementation of consolidated data project management and reporting system for Security Assessment and Audit of projects across all GC departments"),
                t("Facilitated requirements gathering with management and Director level to understand scope and high-level business process"),
                t("Provided knowledge transfer and training to internal FTE staff")
            ],
            "technical_environment": []
        },
        {
            "number": "8.2",
            "title": "Atlassian JIRA Implementation",
            "date_range": {"start": "January 2018", "end": "May 2018"},
            "description": "The client was implementing JIRA for managing and tracking tasks performed by a number of Cyber Security teams. In addition to the JIRA implementation there were complimentary integrated implementations of Confluence and HipChat.",
            "outcomes": "",
            "tasks_performed": [
                t("Reviewed the 'as-is' implementation and align it with the work methodologies and requirements for three teams"),
                t("Created and used a simplified business process mapping and gap analysis strategy and refined key workflows and status types"),
                t("Implementation of consolidated data project management and reporting system for Cyber Threat Management within CITS"),
                t("Defined and implemented JIRA access controls for the Cyber Threat Management team, establishing role-based permission scopes"),
                t("Facilitated requirements gathering with management level to understand scope and high-level business process"),
                t("Implemented Backlog concepts, daily stand-up meetings, and Kanban for visualization"),
                t("Standardized concepts and practices", ["Definition of Ready concepts defined dependencies to be completed before work can commence", "Acceptance Criteria concepts defined core task output requirements", "Definition of Done standardized the concept of describing a task as done within the team", "All concepts were backed by JIRA customization to facilitate checklists"]),
                t("Created and deployed an HA infrastructure into a VMWare ESXI 6 environment"),
                t("Infrastructure was architected using NGINX as a Proxy/Load Balancer with JIRA, Confluence and HipChat instances, backed by PostgreSQL on CentOS 7"),
                t("All data volumes were LUKS encrypted, and traffic encrypted with SSL and properly signed certificates"),
                t("Backups were performed daily via Bash Scripts capturing application, data, and database to a remote backup server"),
                t("Provided knowledge transfer and training to internal FTE staff")
            ],
            "technical_environment": []
        }
    ]
}
data["projects"].append(p8)

# ============================================================
# PROJECT 7
# ============================================================
p7 = {
    "number": 7,
    "title": "Brookfield Renewable Energy Cloud Delivery",
    "client": {"name": "Brookfield Renewable Energy", "department": "", "team": ""},
    "role": "Office 365 & Cloud Delivery Manager",
    "date_range": {"start": "September 2017", "end": "December 2017"},
    "description": "",
    "outcomes": [
        "Provided governance and oversight for Brookfield Renewable Energy's cloud services (Azure, Office 365) vendor consolidation, successfully transitioning multi-MSP support to SoftChoice with no service interruption across a publicly traded, USA Utilities-regulated environment.",
        "Established RBAC and mobile device management (Microsoft InTune) governance framework meeting NIST-equivalent ITSG controls for regulated utility and M&A integration requirements."
    ],
    "technical_environment": [
        te("Cloud", ["Microsoft Office 365", "Microsoft Skype for Business", "Microsoft Azure Cloud", "Azure ExpressRoute", "Azure InTune Mobile Device Management", "Microsoft PowerShell"]),
        te("Servers", ["Windows 2008R2", "Active Directory"])
    ],
    "sub_projects": [
        {
            "number": "7.1",
            "title": "Office 365 and Microsoft Azure Cloud Service Delivery Manager",
            "date_range": {"start": "September 2017", "end": "December 2017"},
            "description": "The client was performing extensive internal change, due to growth via Mergers & Acquisition, requiring a change in support vendor. A consolidation of multiple Managed Service Providers was in flight. The primary objective was to provide guidance and governance to the cloud services (Azure and Office365) support vendor, SoftChoice.",
            "outcomes": "",
            "tasks_performed": [
                t("Provide guidance and governance to the cloud services (Azure and Office365)"),
                t("Provide management and oversight of vendor cloud architecture"),
                t("Oversight and governance for implementation of IT Security to meet NIST controls (eq. ITSG)"),
                t("Governed the Azure AD and Office 365 access control posture during MSP vendor consolidation", ["Office 365", "Azure Active Directory", "Microsoft InTune MDM (Mobile Device Management)", "Azure VNET, VMs, ExpressRoute, LoadBalancing"]),
                t("Provided guidance and governance to Mobile Security Program and Posture to manage roll-out of Microsoft Azure InTune"),
                t("Coordinated transition requirements across Brookfield Renewable Energy business departments and SoftChoice support teams"),
                t("Oversaw workload and workflow migration to Office365, and Azure Cloud"),
                t("Responsible for performance monitoring via standardized KPIs"),
                t("Provided knowledge transfer and training to internal FTE staff"),
                t("Day-to-day management of internal requests and tickets, including Active Directory, on-premise E-mail, and Cisco CUCM")
            ],
            "technical_environment": []
        }
    ]
}
data["projects"].append(p7)

# ============================================================
# PROJECT 6
# ============================================================
p6 = {
    "number": 6,
    "title": "Lowe Martin DevOps",
    "client": {"name": "Lowe Martin Group", "department": "", "team": ""},
    "role": "DevOps",
    "date_range": {"start": "March 2017", "end": "September 2017"},
    "description": "",
    "outcomes": [
        "Restructured Lowe Martin's software development team from unstructured delivery into a functioning Agile/Scrum organization, introducing JIRA-based project management, Definition of Ready/Done standards, and Kanban reporting across IBM WebSphere and Java project streams.",
        "Migrated 2,000+ mail objects (user mailboxes, shared mailboxes, group mailboxes, shared calendars, and resources) from a mixed Microsoft Exchange 2010 / Lotus Domino 9 environment to Office 365 with SIEM-integrated security controls mapped to ISO security standards.",
        "Designed and integrated AWS cloud components (EC2, Auto Scaling, ELB, S3, CloudWatch) for Xerox XMPie Suite deployment supporting print manufacturing workflows."
    ],
    "technical_environment": [
        te("Public Cloud", ["Microsoft Office 365", "Microsoft Skype for Business", "Microsoft Office 365 Compliance", "Amazon AWS Cloud", "AWS VPC", "AWS CloudFront", "AWS CloudWatch", "AWS CloudTrail", "AWS IAM", "AWS EC2", "AWS SES", "AWS S3"]),
        te("Applications", ["Xerox XMPie", "Microsoft SQL Server 2014", "Microsoft PowerShell", "Selenium", "Bash", "Java 8.3", "Tomcat 8.0", "MySQL", "DB2", "Atlassian JIRA", "Atlassian Confluence", "Atlassian HipChat", "BitTitan MigrationWiz", "Exchange 2013", "Lotus Domino 9"]),
        te("Servers", ["Microsoft Windows 2008R2", "Microsoft Windows 2012", "RHEL 6.5"])
    ],
    "sub_projects": [
        {
            "number": "6.1",
            "title": "Dev Ops",
            "date_range": {"start": "March 2017", "end": "September 2017"},
            "description": "The client was performing extensive internal change, which required the re-organization of the Software Development team from an unstructured and chaotic team into a fluid Agile and Scrum based team.",
            "outcomes": "",
            "tasks_performed": [
                t("Project Management using Agile & Scrum techniques"),
                t("Project Management of IBM WebSphere, Java, and UIX projects", ["IBM WebSphere", "DB2 Database", "Java, and .Net application", "CI/CD Pipeline - Jenkins"]),
                t("Project Management of WebSphere Individual Customer Web Store for each customer"),
                t("Configuration and management of Atlassian JIRA and Confluence project and space environments"),
                t("Facilitated Agile workflow requirements with customer service, sales, client, and executive representatives"),
                t("Implementation of consolidated data project management and reporting system for GC Client Departments"),
                t("Architected the Atlassian JIRA permission scheme separating internal staff access from external GC client access"),
                t("Project Planning, Architecture, and Deployment of ITIL based ServiceDesk"),
                t("Provided knowledge transfer and training to internal FTE staff"),
                t("Project Planning, Architecture and Upgrade Deployment of Xerox XMPie Suite", ["Implementation and integration of AWS Cloud components", "Needs analysis, planning and design", "Architecture and Service creation", "Integration with internal systems and automation"]),
                t("AWS Cloud Solution for Imagery Hosting", ["EC2, AutoScaling, Elastic Load Balancing", "S3 Storage, IAM Policies", "CloudWatch and Event Driven Architecture Design"])
            ],
            "technical_environment": []
        },
        {
            "number": "6.2",
            "title": "Office 365 Migration from Exchange & Domino Environments",
            "date_range": {"start": "March 2017", "end": "September 2017"},
            "description": "The client was performing a planned migration from an on-premise mixed environment of Microsoft Exchange 2010 and Lotus Domino 9 to a completely hosted Office 365 environment. The quantity of mail objects was 2000+.",
            "outcomes": "",
            "tasks_performed": [
                t("Internal directory configuration reviews"),
                t("Migration planning and aligning to tool requirements"),
                t("Deployment of Office365 specific features"),
                t("Lotus Domino Migration to Exchange & Manual Migration processes", ["Active Directory Design and Management", "Active Directory Federation Services", "Exchange Online + Litigation/Auditing Features", "Exchange Online Security Configuration and access policies", "Microsoft Office Software and deployment strategies", "Microsoft Skype for Business deployment"]),
                t("Exchange Mailbox and Resource migration processes"),
                t("Implementation of IT Security and Cyber Protection Controls with SIEM integration. Map to ISO Security Controls"),
                t("Implemented the Exchange Online access control framework for 2,000+ migrated mail objects"),
                t("PowerShell scripting and automation"),
                t("Migration Review and end user documentation with cross-training and knowledge transfer")
            ],
            "technical_environment": []
        }
    ]
}
data["projects"].append(p6)

# ============================================================
# PROJECT 5
# ============================================================
p5 = {
    "number": 5,
    "title": "HighRoads US Cloud Migration",
    "client": {"name": "HighRoads (US - Boston, MA)", "department": "", "team": ""},
    "role": "Cloud Transformation & Cloud Architect",
    "date_range": {"start": "January 2017", "end": "April 2017"},
    "description": "",
    "outcomes": [
        "Migrated HighRoads US Exchange environment from multiple M&A-inherited mail servers and domains to a unified Office 365 tenant during IT department restructuring, maintaining HIPAA, NIST, and ISO compliance throughout and enabling full transition to outsourced third-party support with zero mailbox loss.",
        "Migrated HighRoads US Atlassian JIRA and Confluence from on-premise to cloud SaaS, including full migration of historical project data, enabling complete deprecation of on-premise Atlassian infrastructure and supporting IT headcount reduction objectives. Migrated legacy application servers to AWS with automated archiving and on-demand restore capability."
    ],
    "technical_environment": [
        te("Public Cloud", ["Microsoft Office 365", "Microsoft Office 365 Compliance", "Microsoft Skype for Business", "Microsoft SharePoint Online", "Amazon AWS Cloud", "AWS EC2", "AWS RDS", "AWS SES", "AWS S3", "AWS CloudWatch", "AWS CloudFormation", "AWS CloudTrail", "AWS IAM", "AWS Certificate Manager", "AWS WAF"]),
        te("Applications", ["MySQL", "Exchange 2013", "Active Directory", "PowerShell", "Bash", "Atlassian JIRA", "Atlassian Confluence"]),
        te("Servers", ["Microsoft Windows 2008R2", "Microsoft Windows 2012", "VMWare 5.5", "VMWare 6", "RedHat 6.5", "CentOS 6", "CentOS 7"]),
        te("Security", ["Fortinet FortiGate", "Fortinet FortiGuard", "Check Point FW", "F5 Big-IP LTM", "Syslog-NG", "ME EventLog Analyzer"])
    ],
    "sub_projects": [
        {
            "number": "5.1",
            "title": "Exchange Email Cloud Migration",
            "date_range": {"start": "January 2017", "end": "April 2017"},
            "description": "The client was undergoing extensive internal restructuring, right-sizing staffing and migrating services to the cloud to reduce costs and mitigate risks.",
            "outcomes": "",
            "tasks_performed": [
                t("Internal directory configuration reviews"),
                t("Migration planning and aligning to tool requirements"),
                t("Active Directory upgrades & reconfiguration"),
                t("Office365 Tenant Creation and Domain planning"),
                t("Deployment of Office365 specific features", ["Active Directory Design and Management", "Active Directory Federation Services", "Exchange Online + Litigation/Auditing Features", "Exchange Online Security Configuration and access policies", "Microsoft Office Software and deployment strategies", "Microsoft Skype for Business deployment"]),
                t("Exchange Mailbox & Resource Migration & Cutover Process"),
                t("Facilitated requirements gathering with client teams from multiple sites"),
                t("Implementation of IT Security and Cyber Protection Controls. Map to ISO:27001, NIST, and HIPAA"),
                t("Established the Office 365 access control framework for the HighRoads US migration"),
                t("PowerShell scripting and automation"),
                t("Migration Review and end user documentation"),
                t("Decommission of Exchange Server Services"),
                t("Provide documentation, knowledge transfer, and cross-training")
            ],
            "technical_environment": []
        },
        {
            "number": "5.2",
            "title": "Atlassian Project Management Cloud Migration",
            "date_range": {"start": "March 2017", "end": "April 2017"},
            "description": "Client was migrating all on premise services into cloud/SaaS versions to support a change in internal IT Strategy, and re-org reducing IT head count.",
            "outcomes": "",
            "tasks_performed": [
                t("Project Management using Waterfall methodologies"),
                t("Migration planning and needs analysis"),
                t("Production application upgrade path process"),
                t("Test driven change management to remediate cloud feature-function manual configurations"),
                t("Migration process and cut over"),
                t("Bash & SQL Scripting and automation"),
                t("Coordinated migration requirements with development, QA, IT, sales, and executive stakeholders"),
                t("Implementation of IT Security and Cyber Protection Controls. Map to ISO:27001, NIST, and HIPAA"),
                t("Structured the Atlassian JIRA and Confluence access control model for the cloud migration"),
                t("Migration Review and end user documentation"),
                t("End-User enablement for self-serve operations"),
                t("Migration of on-premise servers into AWS cloud"),
                t("On-premise servers decommission"),
                t("AWS Cloud automation for archiving and auto-build & start process for legacy system lookups"),
                t("Provide documentation, knowledge transfer, and cross-training")
            ],
            "technical_environment": []
        }
    ]
}
data["projects"].append(p5)

# ============================================================
# PROJECT 4
# ============================================================
p4 = {
    "number": 4,
    "title": "HighRoads Canada Inc. Infrastructure Operations Manager",
    "client": {"name": "HighRoads Canada Inc. (Ottawa, ON)", "department": "", "team": ""},
    "role": "DevOps, Operations and Cloud Architect; Project Management",
    "date_range": {"start": "June 2015", "end": "December 2016"},
    "description": "",
    "outcomes": [
        "Migrated 40+ production workloads from VMware to AWS, reducing costs by 35% and improving platform resilience. Delivered active-passive HIPAA-compliant DR architecture meeting strict NIST RTO/RPO objectives. Introduced DevOps and automation practices improving deployment frequency by 50% while operationalizing 3 hybrid AWS/on-prem architectures supporting 100+ workloads. Standardized engineering workflows enabling effective collaboration across 15-person off-shore engineering team."
    ],
    "technical_environment": [
        te("Public Cloud", ["Amazon AWS (EC2, ELB, Auto-Scaling, Lambda, S3, EBS, EFS, RDS, VPC, CloudFront, Route53, CloudWatch, CloudTrail, Config, Systems Manager)", "Microsoft Azure", "NaviSite Cloud"]),
        te("Private Data Centre", ["Tier3 certified data centres Rogers Data Centres", "NaviSite Data Centres"]),
        te("Applications", ["Oracle 10g", "MS Exchange", "Active Directory", "OpenLDAP", "PingFed Identity Management", "Atlassian JIRA", "Atlassian Bamboo", "Atlassian Confluence", "Atlassian HipChat", "Nagios Monitoring", "SolarWinds Monitoring", "OpManager Monitoring", "Observium Monitoring", "Syslog-NG", "UniTrends Enterprise Backup", "Microsoft Project 2013", "Gerrit GIT", "Apache SVN", "SALT", "Java", "Tomcat", "Apache", "SOLR", "IIS", ".NET", "Azure PowerShell", "Azure ARM", "AWS CloudFormation"]),
        te("Servers", ["RHN Satellite", "Windows 2008", "Windows 2012", "RedHat RHEL / CentOS 5.5/6.0/7", "VMWare 5.5", "VMWare 6", "Citrix XenServer 6.5"]),
        te("Security", ["Cisco Catalyst", "FortiGate Firewall", "FortiGate FortiGuard", "FortiOS IPS", "CheckPoint Firewall", "CheckPoint IDS/IPS", "F5 Big-IP LTM", "Snort", "Syslog-NG", "rsyslog", "Splunk", "AlienVault", "PFSense SquidGuard", "CheckPoint DLP", "Nagios", "SolarWinds", "Tenable Nessus"])
    ],
    "sub_projects": [
        {
            "number": "4.1",
            "title": "AWS Cloud Migration (In-house custom SaaS platform)",
            "date_range": {"start": "December 2015", "end": "December 2016"},
            "description": "Architected and managed the migration and implementation of on-premise systems into the AWS cloud platform. This involved right-sizing systems, provisioning micro-service based architecture and leveraging cloud-based security principles.",
            "outcomes": "Successfully migrated 40+ production workloads from VMware to AWS, achieving 35% cost reduction through cloud optimization and improved platform resilience.",
            "tasks_performed": [
                t("Project Management using Agile methodologies, and hybrid reporting"),
                t("Needs analysis, define requirements, and plan migration route"),
                t("Architectural design and PoC implementation", ["AWS Cloud, IAM, SQS, SNS, SES", "AWS EC2; Elastic Load Balancing, Auto-Scaling Groups, Lambda", "S3 Storage, Elastic Block Store, Elastic File System", "AWS RDS, EC2 Oracle (BYOD)", "VPC, CloudFront, Route53", "CloudWatch, CloudTrail, Config, SystemsManager, Trusted Advisor", "AWS CloudFormation, TerraForm v0.7, SALT, bespoke scripting, GIT, Bamboo, Jenkins", "Docker - Java/Tomcat Container Applications"]),
                t("Market compliance under HIPAA & NIST guidelines"),
                t("Convened cross-functional working groups spanning development, QA, professional services, IT support, sales, and customer representatives"),
                t("Implementation of IT Security and Cyber Protection Controls. Map to ISO:27001, NIST, and HIPAA"),
                t("Designed the SaaS application access control architecture"),
                t("Review and realign infrastructure with cloud offerings"),
                t("Staged migratory testing of services with inline remediation"),
                t("Internal feedback to development and operations for change coordination"),
                t("Provide final architecture and documentation"),
                t("Provide documentation, knowledge transfer, and cross-training"),
                t("Migration and cut-over processes")
            ],
            "technical_environment": []
        },
        {
            "number": "4.2",
            "title": "SaaS System: DevOps Infrastructure",
            "date_range": {"start": "June 2015", "end": "September 2016"},
            "description": "A traditional hosted customer facing CMS system was in production. Highroads was designing a new V2 system as a fully SaaS product with both web GUI access and customer available API access.",
            "outcomes": "Introduced comprehensive DevOps and automation practices improving deployment frequency by 50% and eliminating manual deployment steps through CI/CD pipeline implementation.",
            "tasks_performed": [
                t("Project Management using Agile methodologies, and hybrid reporting"),
                t("Needs analysis, define requirements, and plan migration route"),
                t("Architectural design and PoC implementation with modernization of infrastructure", ["AWS Cloud, IAM, SQS, SNS, SES", "AWS EC2; Elastic Load Balancing, Auto-Scaling Groups, Lambda", "S3 Storage, Elastic Block Store, Elastic File System", "AWS RDS, EC2 Oracle (BYOD)", "VPC, CloudFront, Route53", "CloudWatch, CloudTrail, Config, SystemsManager, Trusted Advisor", "AWS CloudFormation, TerraForm v0.7, SALT, bespoke scripting, GIT, Bamboo, Jenkins", "VMWare 5.5 & 6.0, Citrix XenServer, Redhat RHEV, RedHat RHEL, Redhat Satellite & Moonwalk", "Docker - Java/Tomcat Container Applications, Syslog-NG, BMC Insights"]),
                t("Security Coordination and alignment to required Guidelines (HIPAA & NIST)"),
                t("Implementation of IT Security and Cyber Protection Controls. Map to ISO:27001, NIST, and HIPAA"),
                t("Extended the access control posture to the DevOps infrastructure layer"),
                t("Led discovery sessions across the 15-person offshore engineering team, QA, and operations staff"),
                t("Pre-migratory pen-testing and security reporting, load testing, and failure/high-availability testing"),
                t("Migration and cut-over processes"),
                t("Documentation preparation for Operations staff, Development staff, and Management")
            ],
            "technical_environment": []
        },
        {
            "number": "4.3",
            "title": "Infrastructure Decommission & Migration",
            "date_range": {"start": "October 2015", "end": "April 2016"},
            "description": "An asset sale required a project to divest software, development environments, QA environments, staging environments, demo environments, training environments, DR environments, and production environments for the V1 software product.",
            "outcomes": "Delivered active-passive HIPAA-compliant DR architecture meeting strict NIST RTO/RPO objectives while ensuring zero downtime migration of production systems.",
            "tasks_performed": [
                t("Project Management using Waterfall methodologies"),
                t("Stakeholder reporting and meetings with C-Level executives and Board Members"),
                t("Needs analysis, define requirements, and plan migration route"),
                t("Architectural design and PoC implementation with modernization of infrastructure", ["AWS Cloud, IAM, SQS, SNS, SES", "AWS EC2; Elastic Load Balancing, Auto-Scaling Groups, Lambda", "S3 Storage, Elastic Block Store, Elastic File System", "AWS RDS, EC2 Oracle (BYOD)", "VPC, CloudFront, Route53", "CloudWatch, CloudTrail, Config, SystemsManager, Trusted Advisor", "AWS CloudFormation, TerraForm v0.7, SALT, bespoke scripting, GIT, Bamboo, Jenkins", "Docker - Java/Tomcat Container Applications, Oracle WebLogic, Oracle 11, Syslog-NG, BMC Insights"]),
                t("Security Coordination and alignment to required Guidelines (HIPAA & NIST)"),
                t("Implementation of IT Security and Cyber Protection Controls. Map to ISO:27001, NIST, and HIPAA"),
                t("Perform safe deconstruction and decommission of legacy data centre and hosted solutions"),
                t("Developed the transitional access control program governing system hand-over"),
                t("Orchestrated joint requirements sessions between selling and purchasing organizations"),
                t("Staged migratory testing of services with inline remediation"),
                t("Pre-migratory pen-testing and security reporting, load testing, and failure/high-availability testing"),
                t("Migration and cut-over processes"),
                t("Decommission of legacy hardware, separation of hardware"),
                t("Project Close-Out, Stakeholder reporting, Legal/Financial reporting for Escrow fund compliance"),
                t("Documentation preparation for Operations staff, Development staff, Management, and external acquiring company")
            ],
            "technical_environment": []
        },
        {
            "number": "4.4",
            "title": "Operations Decommission & Migration",
            "date_range": {"start": "May 2016", "end": "December 2016"},
            "description": "In Q4 2016 Highroads announced the closure of their Canadian offices. IT Operations was to be fully handed over to various outsourced vendors.",
            "outcomes": "Operationalized 3 hybrid AWS/on-prem architectures supporting 100+ workloads with scalable and secure patterns.",
            "tasks_performed": [
                t("Project Management using Waterfall methodologies"),
                t("Stakeholder reporting and meetings with C-Level executives and Board Members"),
                t("Needs analysis, define requirements, and plan migration route"),
                t("Review and realign infrastructure with cloud offerings", ["AWS Cloud, IAM, SQS, SNS, SES", "AWS EC2; Elastic Load Balancing, Auto-Scaling Groups, Lambda", "S3 Storage, Elastic Block Store, Elastic File System", "AWS RDS, EC2 Oracle (BYOD)", "VPC, CloudFront, Route53", "CloudWatch, CloudTrail, Config, SystemsManager, Trusted Advisor", "AWS CloudFormation, TerraForm v0.7, SALT, bespoke scripting, GIT, Bamboo, Jenkins", "Docker - Java/Tomcat Container Applications, Oracle WebLogic, Oracle 11, Syslog-NG, BMC Insights"]),
                t("Security Coordination and alignment to required Guidelines (HIPAA & NIST)"),
                t("Implementation of IT Security and Cyber Protection Controls. Validation of migrated system for HIPAA compliance"),
                t("Develop and implement Access Control Program for migration and hand-over to parent operations in Boston, MA"),
                t("Facilitated decommission and migration requirements across development, operations, legal, and executive teams"),
                t("Staged migratory testing of services with inline remediation"),
                t("Provide final architecture and documentation"),
                t("Migration and cut-over processes"),
                t("Preparation and planning for decommission of legacy hardware"),
                t("Project Close-Out and handover"),
                t("Documentation preparation for Operations staff, Development staff, Management, and external outsourced support company")
            ],
            "technical_environment": []
        }
    ]
}
data["projects"].append(p4)

# ============================================================
# PROJECT 3
# ============================================================
p3 = {
    "number": 3,
    "title": "Dymon Corporation - Infrastructure Manager",
    "client": {"name": "Dymon Corporation", "department": "", "team": ""},
    "role": "Operations and Infrastructure Architect",
    "date_range": {"start": "December 2014", "end": "June 2015"},
    "description": "",
    "outcomes": [
        "Delivered three concurrent infrastructure modernization initiatives across Dymon Corporation's storage, healthcare, and construction business lines within a 7-month engagement, consolidating fragmented physical infrastructure into standardized virtualized platforms.",
        "Achieved PCI-DSS 3.0 and PIPEDA compliance across all Dymon business units through unified security controls spanning POS systems, credit transactions, and healthcare data environments."
    ],
    "technical_environment": [
        te("Public Cloud", ["Microsoft Office 365"]),
        te("Private Data Centre", ["Physical on-premise locations"]),
        te("Applications", ["Active Directory", "SpiceWorks Helpdesk", "SysAid ITIL Helpdesk", "ManageEngine OpManager Monitoring", "Symantec Backup Exec", "UniTrends Backup", "Microsoft Project 2010 Server", "Sage Timberline Suite", "IIS", ".NET", "Shift4 Payment Processing", "DHL Total Recall ERP"]),
        te("Servers", ["Physical Servers", "Citrix XenServer", "VMWare 5.5", "CentOS", "Windows 2003", "Windows 2008", "Windows 2012", "Windows 2008 Terminal Services", "Windows 2012 RDS"]),
        te("Networking", ["Cisco Switches", "HP ProCurve"]),
        te("Security", ["Sophos UTM (NextGen FW)", "rsyslog", "Syslog-NG", "SolarWinds", "ME OpManager Monitoring"])
    ],
    "sub_projects": [
        {
            "number": "3.1",
            "title": "Operations Virtualization",
            "date_range": {"start": "December 2014", "end": "May 2015"},
            "description": "The Dymon corporate infrastructure was operating on unique physical hardware per server and per service. Analysis identified 8 physical servers of identical capacity running at less than 20% utilization.",
            "outcomes": "Consolidated 8 underutilized physical servers into a Citrix XenServer virtualized cluster, reclaiming 3 unused Layer 3 switches. Implemented VLAN-segmented network architecture with PCI-DSS 3.0 compliance.",
            "tasks_performed": [
                t("Stakeholder reporting and meetings with CIO"),
                t("Needs analysis, define requirements, and plan migration route"),
                t("Review and realign infrastructure plan with budget limitations", ["HP ProCurve Switching with Cisco Top-of-Rack Switches & Sophos UTM", "HP Switching and MPLS Integration", "WhiteBox Server Hardware Cluster", "Citrix XenServer Clustering & Replicated NAS Storage", "Linux CentOS Workload Servers"]),
                t("Security Coordination and alignment to required Guidelines (PCI Compliance)"),
                t("Implementation of IT Security and Cyber Protection Controls with compliance to PCI-DSS 3.0"),
                t("Facilitated requirements gathering within organization with consideration to distributed workforce"),
                t("Staged migratory testing of services with inline remediation"),
                t("Migration and cut-over processes"),
                t("Preparation and planning for decommission of legacy hardware"),
                t("Project Close-Out and handover"),
                t("Documentation preparation for Operations staff including cross-training and knowledge transfer")
            ],
            "technical_environment": []
        },
        {
            "number": "3.2",
            "title": "Remote Desktop Services (RDS) / Thin Client Implementation",
            "date_range": {"start": "January 2015", "end": "June 2015"},
            "description": "The Dymon Health Care retirement residences were operating with heavily aged systems. A Terminal Server (RDS) / Thin Client model was selected to provide roaming profiles for nursing staff while centralizing data on corporate servers.",
            "outcomes": "Replaced aging multi-OS desktop infrastructure with centralized Citrix XenServer and Windows 2012 R2 RDS thin client solution. Centralized user data and roaming profiles achieving PIPEDA compliance for healthcare data.",
            "tasks_performed": [
                t("Stakeholder reporting and meetings with CIO & Health Care COO"),
                t("Needs analysis, define requirements, and plan transformation", ["Citrix XenServer Virtualization Cluster & Defined NAS Storage Cluster", "Windows 2012 R2 Remote Desktop Services Cluster", "Active Directory design and management for isolation of RDS Users", "WyseTerminal Hardware & Virtual Terminals on existing hardware"]),
                t("Security Coordination and advisory process"),
                t("Staged migratory testing of services with inline remediation"),
                t("Migration and cut-over processes"),
                t("Implementation of IT Security and Cyber Protection Controls with compliance to Canadian PIPEDA"),
                t("Preparation and planning for repurposing or decommission of legacy hardware"),
                t("Project Close-Out and handover"),
                t("Documentation preparation for Operations staff including knowledge transfer and cross-training")
            ],
            "technical_environment": []
        },
        {
            "number": "3.3",
            "title": "Sales Software & POS Infrastructure System Upgrade",
            "date_range": {"start": "May 2015", "end": "June 2015"},
            "description": "A vendor driven change to end-user credit transaction PIN pads required Dymon Storage to update their credit transaction software, Line of Business integration module, merchant banking authentication and physical handsets with zero downtime.",
            "outcomes": "Executed vendor-mandated PIN pad replacement and credit transaction software upgrade across all Dymon Storage facilities with zero downtime. Maintained PCI-DSS 3.0 compliance throughout the upgrade cycle.",
            "tasks_performed": [
                t("Stakeholder reporting and meetings with CIO, COO, and Chief Accountant"),
                t("Needs analysis, define requirements, and plan transformation"),
                t("Security Coordination and advisory process"),
                t("Lab-based PoC testing"),
                t("Migration and cut-over processes"),
                t("Implementation of IT Security and Cyber Protection Controls with compliance to PCI-DSS 3.0"),
                t("Facilitated requirements gathering within organization with healthcare operations"),
                t("Map high-level business processes and engage with key team-leads for gap analysis"),
                t("Project Close-Out and handover"),
                t("Documentation preparation for Operations staff including cross-training and knowledge transfer")
            ],
            "technical_environment": []
        }
    ]
}
data["projects"].append(p3)

# ============================================================
# PROJECT 2
# ============================================================
p2 = {
    "number": 2,
    "title": "GeoDigital International Inc. Infrastructure Manager",
    "client": {"name": "GeoDigital International (GeoSpatial Engineering)", "department": "", "team": ""},
    "role": "Operations and Infrastructure Architect",
    "date_range": {"start": "September 2011", "end": "December 2014"},
    "description": "",
    "outcomes": [
        "Successfully designed and deployed GIS SaaS platform on AWS serving 500+ global clients across 15 countries with 99.5% uptime. Engineered 1-2 TB/day data ingestion pipeline improving engineering timelines by 50%, while managing infrastructure operations for 8 production and engineering environments supporting 25+ engineering staff with 99.8% data processing reliability."
    ],
    "technical_environment": [
        te("Public Cloud", ["Amazon AWS (EC2, S3, ELB, AutoScaling, CloudFront, CloudWatch, SNS, SES)", "RackSpace Cloud", "Microsoft Azure", "Microsoft Office 365", "Google GCP"]),
        te("Multi-Region Deployment", ["15 countries globally with cloud-native architecture"]),
        te("Data Processing", ["1-2 TB/day automated ingestion pipeline with 99.8% reliability"]),
        te("Platform Scale", ["500+ global clients with 99.5% uptime across 8 production environments"]),
        te("Private Data Centre", ["Physical on-premise location", "Rogers Tier 2", "ATT Tier 3"]),
        te("Applications", ["Multiple GIS Platforms", "SharePoint", "QuickBase", "SalesForce", "MS SQL", "MySQL", "MS Exchange 2010", "Active Directory", "ManageEngine ServiceDesk Pro", "ManageEngine OpManager Monitoring", "Symantec BackupExec", "Veeam Backup", "Microsoft Project 2010", "VisualSVN"]),
        te("Servers", ["Windows 2008 R2", "Windows 2012", "VMWare 5.5", "Linux KVM", "RedHat RHEV", "Microsoft Hyper-V", "Citrix XenServer"]),
        te("Networking", ["Cisco Catalyst", "Cisco IOS Routers", "Dell PowerConnect"]),
        te("Security", ["Cisco ASA", "FortiNet FortiGate", "Snort", "F5 Big-IP LTM", "Nagios", "Solar Winds", "New Relic Monitoring", "ME OpManager Monitoring"])
    ],
    "sub_projects": [
        {
            "number": "2.1",
            "title": "PAS - Photo Acquisition Service SaaS Cloud Application",
            "date_range": {"start": "May 2012", "end": "December 2014"},
            "description": "GeoDigital created a market pioneering SaaS application utilized by premium US insurance companies to provide a Photo Acquisition Service (PAS) system to provide on-the-fly imagery and extrapolated engineering metrics for roofing claims.",
            "outcomes": "Successfully deployed market-leading SaaS platform serving 500+ global insurance company clients across 15 countries with 99.5% platform uptime.",
            "tasks_performed": [
                t("Project managed and deliverables tracked with Agile Project methodologies and Sprint based cadences"),
                t("Needs analysis, define requirements, and identify cloud provider (AWS & RackSpace)"),
                t("Architectural design and PoC implementation", ["AWS EC2 Linux Instances & AWS EC2 Windows Instances", "AWS ELB Load Balancers & AutoScaling & AWS CloudFront", "AWS S3 Storage & AWS EC2 EBS", "AWS CloudWatch & AWS SNS & AWS SES", "Secure data links & delivery redirected to On-Premise Datacentre"]),
                t("Security Coordination and alignment to required Guidelines (NERC, FISMA & NIST)"),
                t("Implementation of IT Security and Cyber Protection Controls. Compliance required for ISO:27001, NERC and NIST"),
                t("Partnered with R&D team and flagship early-adopter insurance client to define SaaS product workflows"),
                t("Established the SaaS platform access control framework defining RBAC roles"),
                t("Staged build and deployment of cloud infrastructure and on-premise infrastructure"),
                t("Internal integration to CI/CD pipeline, automation, and management systems", ["Automation Scripting (Bash, Python, MS Batch)", "Hudson-Jenkins CI/CD Tooling", "Visual SVN Subversion Version-Control System"]),
                t("Generate final architecture and documentation"),
                t("Pre-migratory pen-testing and security reporting, load testing, and failure/high-availability testing"),
                t("Go-Live and release"),
                t("Documentation preparation for Operations staff, Development staff, and Management")
            ],
            "technical_environment": []
        },
        {
            "number": "2.2",
            "title": "Data Centre Migration (Vancouver, BC - Ottawa, ON)",
            "date_range": {"start": "May 2012", "end": "September 2012"},
            "description": "The client required the migration of physical data centre from Vancouver On-Premise location to Ottawa Tier 2 Data Center. Architecture migration of 750TB production IBM FC SAN storage, 200TB Backup/Archival Storage, 2000 Windows 2008R2 Servers, and VMWare 5.0 IBM Cluster.",
            "outcomes": "Successfully migrated 750TB production IBM FC SAN, 200TB backup/archival storage, and 2,000 Windows servers from Vancouver to Ottawa Tier 2 data centre under an expedited timeline with full data integrity preserved.",
            "tasks_performed": [
                t("Project Management using hybrid Agile and waterfall methodologies"),
                t("Needs analysis, define requirements, and extreme risk with project"),
                t("Vendor Selection Advisory and Vendor Engagement"),
                t("Vendor Management & Project Management with focus to high risk"),
                t("Provisioning of supporting infrastructure and data centre services", ["IBM SAN & Brocade FC Switch Fabric", "IBM Tivoli Backup System & IBM SAN & LTO5 Tape Array", "IBM VMWare HyperVisor Cluster & Microsoft Windows 2012 Cluster", "Child Workload VMs of various nature (LiDAR Processing & related)", "Dell PowerConnect Network Switching & Cisco Top of Rack Switching"]),
                t("Coordination and advisory services to organization departments"),
                t("Generate final architecture and supporting documentation"),
                t("Pre-migratory planned tasks, including risk mitigation processes"),
                t("Migratory cut-over including on-site management"),
                t("Post-migration management of changes and integrations"),
                t("Implementation of IT Security and Cyber Protection Controls. Compliance required for ISO:27001, NERC and NIST"),
                t("Coordinated migration impact assessments across production, acquisition, sales, PMO, and executive teams"),
                t("Implemented the post-migration access control posture for the Ottawa data centre"),
                t("Documentation preparation for Operations staff, Production staff, and Management")
            ],
            "technical_environment": []
        },
        {
            "number": "2.3",
            "title": "Corporate Private Cloud (Data Centre Architecture)",
            "date_range": {"start": "September 2012", "end": "August 2013"},
            "description": "As a multi-petabyte data handling organization, GeoDigital required a robust solution for handling data archiving, data retention, and data integrity.",
            "outcomes": "Architected and deployed multi-petabyte corporate private cloud leveraging Tier II and III data centres with NexentaStor software-defined storage. Achieved ISO:27001, NERC, FISMA, and NIST compliance.",
            "tasks_performed": [
                t("Project Management using hybrid Agile & Waterfall methodologies"),
                t("Stakeholder reporting and meetings with Executive teams and operations teams"),
                t("Needs analysis, define requirements for project"),
                t("Advisory services for technology selection and cloud provider integrations"),
                t("Architectural design and lightweight PoC implementation", ["Dell PowerConnect Network Switching & Cisco Top-of-Rack switching", "Dell PowerEdge Server Clusters & Bespoke Dell PowerVault Rack", "NexentaStor Software Defined Storage Cluster", "Redhat Linux RHEL & CentOS Linux Cluster and Virtualization (Xen & KVM)", "Integration with AWS Cloud for off-site replication using AWS S3 buckets"]),
                t("Security Coordination and alignment to required Guidelines (NERC, FISMA & NIST)"),
                t("Implementation of IT Security and Cyber Protection Controls. Compliance required for ISO:27001, NERC and NIST"),
                t("Engaged all business units to capture data archival, retention, and integrity requirements"),
                t("Defined the private cloud access control model"),
                t("Vendor Selection Advisory and Vendor Engagement"),
                t("Vendor Management & Project Management"),
                t("Provide final architecture and documentation"),
                t("Build, deploy and integrate process"),
                t("Project Close-Out"),
                t("Documentation preparation for Operations staff")
            ],
            "technical_environment": []
        },
        {
            "number": "2.4",
            "title": "On-Premise Data Centre Virtualization",
            "date_range": {"start": "September 2012", "end": "August 2013"},
            "description": "Due to growth by corporate acquisitions, the client operated multiple physical locations without a centralized standardized IT Infrastructure platform. This project managed the migration to a standardized Hyper-V virtualization platform.",
            "outcomes": "Standardized fragmented IT infrastructure across multiple physical locations onto a unified Hyper-V virtualization platform. Delivered full license management and auditing achieving ISO:27001, NERC, and NIST compliance.",
            "tasks_performed": [
                t("Project Management using hybrid Agile & Waterfall methodologies"),
                t("Stakeholder reporting and meetings with Executive teams"),
                t("Needs analysis, define requirements for project"),
                t("Architectural design and structure planning", ["Dell PowerConnect Network Switching & Cisco Top-of-Rack switching", "Dell PowerEdge Server Clusters & Bespoke Dell PowerVault Rack", "NexentaStor Software Defined Storage Cluster", "VMWare 5.x Virtualization Cluster", "Integration with AWS Cloud for off-site replication using AWS S3 buckets"]),
                t("Security Coordination and alignment to required Guidelines (NERC, FISMA & NIST)"),
                t("Implementation of IT Security and Cyber Protection Controls. Compliance required for ISO:27001, NERC and NIST"),
                t("Develop and implement Access Control Program based on RBAC requirements with Active Directory integrations"),
                t("Conducted requirements workshops across LiDAR production, QA, field acquisition, and IT support teams"),
                t("Vendor Selection Advisory and Vendor Engagement"),
                t("Provide final architecture and documentation"),
                t("Build, deploy and integrate process"),
                t("Project Close-Out"),
                t("Documentation preparation for Operations staff")
            ],
            "technical_environment": []
        },
        {
            "number": "2.5",
            "title": "Corporate Hybrid Cloud (Production & Field Acquisition Systems)",
            "date_range": {"start": "December 2013", "end": "September 2014"},
            "description": "The client expanded operations into the Australasia region. Leveraging public cloud partners in Sydney, Australia (RackSpace), AWS US, colocation Data Centre partners (Rogers) and on-premises to create an end-to-end data management system for acquisition data at 1-2 TB per day.",
            "outcomes": "Engineered automated 1-2 TB/day data ingestion pipeline improving engineering processing timelines by 50% through multi-cloud architecture. Achieved 99.8% data processing reliability across global cloud partners.",
            "tasks_performed": [
                t("Project Management using hybrid Agile and waterfall methodologies"),
                t("Needs analysis, define requirements, and identify cloud providers"),
                t("Architectural design and PoC implementation with multi-vendor integration", ["RackSpace Compute Instances & Database Instances", "RackSpace Data Ingestion (Up to 2TB per day) at Sydney data centre", "Automated Data validation, manifest validation and replication into AWS Cloud", "AWS EC2 Linux Instances", "AWS ELB Load Balancers & AutoScaling & AWS CloudFront", "AWS S3 Storage & AWS EC2 EBS", "AWS CloudWatch & AWS SNS & AWS SES", "Data replication to off-shore analysts in Asia and in-house analysts in California, Minnesota, British Columbia & Ottawa"]),
                t("Security Coordination and alignment to required Guidelines (NERC, FISMA & NIST)"),
                t("Implementation of IT Security and Cyber Protection Controls. Compliance required for ISO:27001 and NIST"),
                t("Gathered requirements from field acquisition teams in Australia, production staff in North America, and offshore data analysts in Asia"),
                t("Architected the hybrid cloud access control framework spanning RackSpace Sydney, AWS US, and on-premises"),
                t("Staged build and deployment of cloud infrastructure and on-premise infrastructure"),
                t("Internal integration to CI/CD pipeline, automation, and management systems"),
                t("Generate final architecture and documentation"),
                t("Pre-migratory pen-testing and security reporting, load testing, and failure/high-availability testing"),
                t("Go-Live and release"),
                t("Documentation preparation for Operations staff, Development staff, and Management")
            ],
            "technical_environment": []
        },
        {
            "number": "2.6",
            "title": "Office 365 Cloud Migration",
            "date_range": {"start": "September 2011", "end": "December 2012"},
            "description": "The client intended to manage risk and centralize mail management into a streamlined cloud platform after growth through mergers and acquisitions.",
            "outcomes": "",
            "tasks_performed": [
                t("Project Management using hybrid Agile and waterfall methodologies"),
                t("Internal directory configuration reviews"),
                t("Migration planning and aligning to tool requirements"),
                t("Active Directory upgrades & reconfiguration"),
                t("Office365 Tenant Creation and Domain planning"),
                t("Deployment of Office365 specific features"),
                t("Exchange Mailbox & Resource Migration & Cutover Process"),
                t("PowerShell scripting and automation"),
                t("Implementation of IT Security and Cyber Protection Controls. Map to ISO:27001 and NIST"),
                t("Provide guidance and governance for Access Control Program for Microsoft Exchange Mail System"),
                t("Coordinated Exchange migration requirements with key users, IT staff, and management"),
                t("Migration Review and end user documentation"),
                t("Decommission of Exchange Server Services"),
                t("Operational support and maintenance")
            ],
            "technical_environment": []
        }
    ]
}
data["projects"].append(p2)

# ============================================================
# PROJECT 1
# ============================================================
p1 = {
    "number": 1,
    "title": "Central Wire Industries Infrastructure Manager",
    "client": {"name": "Central Wire Industries", "department": "Infrastructure & Operations", "team": ""},
    "role": "Operations and Infrastructure Management",
    "date_range": {"start": "May 2007", "end": "September 2011"},
    "description": "",
    "outcomes": [],
    "technical_environment": [
        te("Private Data Centre", ["Physical on-premise location"]),
        te("Applications", ["SharePoint", "SalesForce", "MS SQL", "MySQL", "Oracle 9", "MS Exchange 2007", "Active Directory", "ManageEngine ServiceDesk Pro", "ManageEngine OpManager Monitoring", "Symantec BackupExec", "Lawson MOVEX (M3)", "Info BPCS", "Infor Syteline"]),
        te("Servers", ["Windows 2003", "Windows 2008", "SCO Unix", "AS/400", "IBM WebSphere"]),
        te("Networking", ["Cisco Catalyst", "Cisco IOS Routers"]),
        te("Security", ["Cisco ASA", "Nagios", "Solar Winds", "ME OpManager Monitoring", "rsyslog", "Syslog-NG"])
    ],
    "sub_projects": [
        {
            "number": "1.1",
            "title": "IT Integration of fully automated production systems (Fond du Lac, Wisconsin)",
            "date_range": {"start": "January 2010", "end": "March 2011"},
            "description": "Central Wire Industries, as a $500 million annual revenue enterprise, expanded its operations with purchase of a smart-factory requiring integration of all aspects of automation, including IT Systems, ERP and MRP systems.",
            "outcomes": "Integrated GE Fanuc smart-factory automation and SCADA systems into centralized AS/400-based Lawson Movex (M3) and Info BPCS ERP/MRP suites. Delivered IT infrastructure supporting lights-out manufacturing operations. Implemented IT security controls meeting US DOD NOFORN classification with ISO:27001 and NIST compliance.",
            "tasks_performed": [
                t("Project Management using waterfall methodologies"),
                t("Needs analysis, define requirements, and trusted vendors"),
                t("Identify additional requirements to support lights-out manufacturing plant"),
                t("Vendor Management and advisory services for integration"),
                t("Management and facilitation of on-premise automation system configuration with Plant Manager"),
                t("Architect, design, and implement IT automation routines for data transfer to centralized AS/400 systems"),
                t("Integration of SNMP monitoring to smart-factory systems plus regular IT Infrastructure"),
                t("Fail-over testing planning and testing to verify on-site documentation comprehensiveness"),
                t("Facilitated requirements gathering between facility production, management, corporate production, material purchasing, external vendors, and IT teams"),
                t("Implementation of IT Security and Cyber Protection Controls including US DOD NOFORN classification. Compliance required for ISO:27001 and NIST"),
                t("Generate final architecture and documentation"),
                t("Go-Live and release")
            ],
            "technical_environment": []
        },
        {
            "number": "1.2",
            "title": "ADP Payroll Systems Migration (Citrix Virtualization, Platform Upgrade, Database Migration)",
            "date_range": {"start": "January 2010", "end": "March 2011"},
            "description": "The client had expanded its market share and physical locations by 60%, onboarding nine physical sites across the United States and Canada. ADP was selected for consolidated payroll services.",
            "outcomes": "Consolidated ADP payroll services across 9 physical sites in the United States and Canada following 60% growth, delivering cross-border HR and Finance access via Citrix virtualization. Implemented RBAC access controls meeting ISO:27001 and NIST compliance.",
            "tasks_performed": [
                t("Project Management using waterfall methodologies"),
                t("Needs analysis, define requirements, and vendors requirements"),
                t("Vendor Management and advisory services for integration"),
                t("Architectural design and implementation planning"),
                t("Security Coordination and alignment for finance and payroll requirements"),
                t("Vendor Engagement and coordination"),
                t("Provisioning of supporting infrastructure and Citrix Desktop streaming services"),
                t("Staged integration of new services with existing infrastructure, and inline remediation"),
                t("Cutover and migration of data and access"),
                t("Facilitated requirements gathering between HR teams, finance teams, executives, external vendors and IT teams"),
                t("Implementation of IT Security and Cyber Protection Controls. Compliance required for ISO:27001 and NIST"),
                t("Provide guidance and governance for Access Control Program for Corporate HR and Payroll systems with RBAC"),
                t("Provide final architecture and documentation"),
                t("Build, deploy and integrate process"),
                t("Project Close-Out"),
                t("Documentation preparation and training for Operations staff, HR Staff, and Finance Staff")
            ],
            "technical_environment": []
        }
    ]
}
data["projects"].append(p1)

# ============================================================
# TECHNOLOGY INDEX
# ============================================================
tech_index = [
    {"name": "Active Directory", "project_references": ["1", "2", "3", "4", "6", "7", "12", "13"]},
    {"name": "ADP Payroll Systems", "project_references": ["1"]},
    {"name": "AlienVault", "project_references": ["4"]},
    {"name": "Apache", "project_references": ["2", "8", "9"]},
    {"name": "Apache SVN", "project_references": ["4"]},
    {"name": "ArgoCD", "project_references": ["13.1", "13.2"]},
    {"name": "Argo Workflows", "project_references": ["13.1", "13.2"]},
    {"name": "Atlassian Bamboo", "project_references": ["4"]},
    {"name": "Atlassian Confluence", "project_references": ["4", "5", "6", "8", "10", "13"]},
    {"name": "Atlassian HipChat", "project_references": ["4", "6"]},
    {"name": "Atlassian JIRA", "project_references": ["4", "5", "6", "8", "10", "13"]},
    {"name": "AWS (Amazon Web Services)", "project_references": ["2", "4", "5", "6", "9", "10", "11", "12", "13"]},
    {"name": "AWS Certificate Manager", "project_references": ["10", "11"]},
    {"name": "AWS CloudFormation", "project_references": ["10", "11", "12", "13"]},
    {"name": "AWS CloudFront", "project_references": ["6", "10", "11"]},
    {"name": "AWS CloudTrail", "project_references": ["6", "10", "11", "13.2"]},
    {"name": "AWS CloudWatch", "project_references": ["6", "10", "11", "13.2"]},
    {"name": "AWS CodeBuild", "project_references": ["11"]},
    {"name": "AWS CodeCommit", "project_references": ["10", "11", "12"]},
    {"name": "AWS CodeDeploy", "project_references": ["10", "11", "12.1", "12.2"]},
    {"name": "AWS CodePipeline", "project_references": ["11"]},
    {"name": "AWS Config", "project_references": ["11", "13.2"]},
    {"name": "AWS Control Tower", "project_references": ["13.2"]},
    {"name": "AWS ECS", "project_references": ["11"]},
    {"name": "AWS EKS (Elastic Kubernetes Service)", "project_references": ["13.1", "13.2"]},
    {"name": "AWS GuardDuty", "project_references": ["11", "13.2"]},
    {"name": "AWS IAM", "project_references": ["6", "10", "11"]},
    {"name": "AWS Lambda", "project_references": ["4", "12", "13", "13.2"]},
    {"name": "AWS Organizations", "project_references": ["11", "13.2"]},
    {"name": "AWS RDS", "project_references": ["11"]},
    {"name": "AWS S3", "project_references": ["6", "11"]},
    {"name": "AWS SES", "project_references": ["6", "11"]},
    {"name": "AWS SSO", "project_references": ["11", "13.2"]},
    {"name": "AWS Systems Manager", "project_references": ["11"]},
    {"name": "AWS Transit Gateway", "project_references": ["11", "13.2"]},
    {"name": "AWS VPC", "project_references": ["6", "10", "11", "13.2"]},
    {"name": "AWS X-Ray", "project_references": ["13.2"]},
    {"name": "Azure", "project_references": ["4", "7", "8", "12"]},
    {"name": "Azure Active Directory", "project_references": ["7", "11", "12", "13"]},
    {"name": "Azure CLI", "project_references": ["8"]},
    {"name": "Azure DevOps", "project_references": ["11", "12", "13"]},
    {"name": "Azure ExpressRoute", "project_references": ["7"]},
    {"name": "Azure InTune", "project_references": ["7"]},
    {"name": "Azure PowerShell", "project_references": ["4", "7", "8"]},
    {"name": "Azure Resource Manager (ARM)", "project_references": ["4", "8"]},
    {"name": "Azure Sentinel", "project_references": ["12.1"]},
    {"name": "Bash", "project_references": ["2", "4", "6", "8", "9", "10", "11", "12", "13"]},
    {"name": "BitTitan MigrationWiz", "project_references": ["6"]},
    {"name": "CDK (AWS Cloud Development Kit)", "project_references": ["11", "13"]},
    {"name": "CDK8s", "project_references": ["13"]},
    {"name": "CentOS", "project_references": ["3", "4", "8", "9", "10", "11", "12", "13"]},
    {"name": "Certificate Manager (AWS)", "project_references": ["10", "11"]},
    {"name": "Check Point", "project_references": ["4", "6"]},
    {"name": "Checkov Security Scanning", "project_references": ["12", "13"]},
    {"name": "Cilium", "project_references": ["13.2"]},
    {"name": "Cisco ASA", "project_references": ["1", "2"]},
    {"name": "Cisco Catalyst", "project_references": ["1", "3"]},
    {"name": "Cisco IOS", "project_references": ["1"]},
    {"name": "CIS Hardening", "project_references": ["12", "13"]},
    {"name": "Citrix XenServer", "project_references": ["1", "2", "3"]},
    {"name": "CloudFlare", "project_references": ["8", "9"]},
    {"name": "CloudFormation", "project_references": ["10", "11", "12", "13"]},
    {"name": "CloudFront", "project_references": ["6", "10", "11"]},
    {"name": "CloudTrail", "project_references": ["6", "10", "11", "13.2"]},
    {"name": "CloudWatch", "project_references": ["6", "10", "11", "13.2"]},
    {"name": "Crossplane", "project_references": ["13.1", "13.2"]},
    {"name": "DB2", "project_references": ["6"]},
    {"name": "Docker", "project_references": ["4", "9", "10", "13.1", "13.2"]},
    {"name": "Docker Images", "project_references": ["13.2"]},
    {"name": "EKS (Elastic Kubernetes Service)", "project_references": ["13.1", "13.2"]},
    {"name": "Elasticsearch", "project_references": ["9", "13.2"]},
    {"name": "Exchange", "project_references": ["1", "5", "6"]},
    {"name": "F5 Big-IP LTM", "project_references": ["1", "2", "4", "6"]},
    {"name": "FortiGate", "project_references": ["1", "2", "4", "6"]},
    {"name": "FortiGuard", "project_references": ["4", "6"]},
    {"name": "FortiOS IPS", "project_references": ["4"]},
    {"name": "GCDOCS", "project_references": ["8"]},
    {"name": "Gerrit GIT", "project_references": ["4"]},
    {"name": "Git", "project_references": ["9", "11", "12", "13"]},
    {"name": "GitLab", "project_references": ["10", "11"]},
    {"name": "GitHub", "project_references": ["11"]},
    {"name": "GitOps", "project_references": ["13.1", "13.2"]},
    {"name": "Golang", "project_references": ["13.1", "13.2"]},
    {"name": "Grafana", "project_references": ["13.2"]},
    {"name": "Helm", "project_references": ["13.1", "13.2"]},
    {"name": "HIPAA Compliance", "project_references": ["4"]},
    {"name": "HP ProCurve", "project_references": ["2"]},
    {"name": "IIS", "project_references": ["4"]},
    {"name": "Info BPCS", "project_references": ["1"]},
    {"name": "Infor Syteline", "project_references": ["1"]},
    {"name": "Infrastructure as Code (IaC)", "project_references": ["10", "11", "12", "13"]},
    {"name": "ITSG Compliance", "project_references": ["11", "13"]},
    {"name": "Java", "project_references": ["4", "6", "9"]},
    {"name": "Jenkins", "project_references": ["2", "4", "6", "9", "10"]},
    {"name": "JFROG Artifactory", "project_references": ["12.2"]},
    {"name": "JSON", "project_references": ["13.2"]},
    {"name": "Kafka", "project_references": ["10"]},
    {"name": "KCL (Configuration Language)", "project_references": ["13.2"]},
    {"name": "Kubernetes", "project_references": ["13.1", "13.2"]},
    {"name": "kubeadm", "project_references": ["13"]},
    {"name": "kind", "project_references": ["13"]},
    {"name": "k3d", "project_references": ["13"]},
    {"name": "Lawson MOVEX (M3)", "project_references": ["1"]},
    {"name": "Load Balancers", "project_references": ["8", "13.2"]},
    {"name": "Lotus Domino", "project_references": ["6"]},
    {"name": "ManageEngine", "project_references": ["1", "9", "10"]},
    {"name": "Microsoft Office 365", "project_references": ["5", "6", "7", "9"]},
    {"name": "Microsoft PowerShell", "project_references": ["4", "6", "7", "8"]},
    {"name": "Microsoft Project", "project_references": ["4"]},
    {"name": "Microsoft SQL Server", "project_references": ["1", "6"]},
    {"name": "Microsoft Windows", "project_references": ["1", "2", "3", "4", "7", "10", "11", "12"]},
    {"name": "MySQL", "project_references": ["1", "6", "9"]},
    {"name": "Nagios", "project_references": ["1", "2", "4"]},
    {"name": ".NET", "project_references": ["4"]},
    {"name": "New Relic", "project_references": ["2"]},
    {"name": "NIST Compliance", "project_references": ["4", "10", "11"]},
    {"name": "OCI Bundles", "project_references": ["13.2"]},
    {"name": "Office 365", "project_references": ["5", "6", "7", "9"]},
    {"name": "OpenLDAP", "project_references": ["4", "9", "10"]},
    {"name": "OpManager", "project_references": ["1", "2", "9"]},
    {"name": "Oracle", "project_references": ["1", "4"]},
    {"name": "PHP", "project_references": ["10"]},
    {"name": "PingFed Identity Management", "project_references": ["4"]},
    {"name": "PostgreSQL", "project_references": ["8", "9", "10"]},
    {"name": "PowerShell", "project_references": ["4", "6", "7", "8"]},
    {"name": "Prisma", "project_references": ["12", "13"]},
    {"name": "Prometheus", "project_references": ["13.2"]},
    {"name": "Python", "project_references": ["9", "13.1", "13.2"]},
    {"name": "RDS (Remote Desktop Services)", "project_references": ["3"]},
    {"name": "RedHat RHEL", "project_references": ["4", "6"]},
    {"name": "RHN Satellite", "project_references": ["4"]},
    {"name": "rsyslog", "project_references": ["1", "2", "4"]},
    {"name": "SALT", "project_references": ["4"]},
    {"name": "SCO Unix", "project_references": ["1"]},
    {"name": "Selenium", "project_references": ["6"]},
    {"name": "SharePoint", "project_references": ["1", "8"]},
    {"name": "Skype for Business", "project_references": ["6", "7", "9"]},
    {"name": "Snort", "project_references": ["1", "2", "4"]},
    {"name": "SOGO", "project_references": ["10"]},
    {"name": "SolarWinds", "project_references": ["1", "2", "4"]},
    {"name": "SOLR", "project_references": ["4"]},
    {"name": "SonarQube", "project_references": ["12.2"]},
    {"name": "Sophos UTM", "project_references": ["2"]},
    {"name": "Splunk", "project_references": ["4"]},
    {"name": "Symantec BackupExec", "project_references": ["1"]},
    {"name": "Syslog-NG", "project_references": ["1", "2", "4", "6"]},
    {"name": "Tenable Nessus", "project_references": ["4"]},
    {"name": "TerraScan", "project_references": ["12"]},
    {"name": "Terraform", "project_references": ["9", "10", "11", "12.1", "13.1", "13.2"]},
    {"name": "Tomcat", "project_references": ["4", "6", "8", "9"]},
    {"name": "TypeScript", "project_references": ["13.1", "13.2"]},
    {"name": "UniTrends", "project_references": ["4"]},
    {"name": "VMware", "project_references": ["1", "2", "3", "4", "8"]},
    {"name": "VMware ESXI", "project_references": ["4", "8"]},
    {"name": "WatchGuard", "project_references": ["8"]},
    {"name": "WebSphere", "project_references": ["1"]},
    {"name": "Windows Server", "project_references": ["1", "2", "3", "4", "7", "10", "11", "12"]},
    {"name": "WSO2", "project_references": ["10"]},
    {"name": "Xerox XMPie", "project_references": ["6"]},
    {"name": "YAML", "project_references": ["13.2"]}
]
data["technology_index"] = tech_index

# Write the JSON file
output_path = "/Users/christian/git-repos/OCC-github/CV/data/raw/cv_data.json"
with open(output_path, 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"Written {output_path}")
print(f"Projects: {len(data['projects'])}")
print(f"Technology index entries: {len(data['technology_index'])}")
total_sub = sum(len(p['sub_projects']) for p in data['projects'])
print(f"Total sub-projects: {total_sub}")
