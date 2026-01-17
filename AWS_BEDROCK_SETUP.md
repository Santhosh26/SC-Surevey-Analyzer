# AWS Bedrock Setup Guide

This guide will help you configure AWS Bedrock to use Claude Opus 4.5 for generating AI-powered survey insights.

## Prerequisites

- AWS account with administrative access
- Python 3.8+ with boto3 library

## Authentication Methods

AWS Bedrock supports two authentication methods:

1. **🌟 AWS Bedrock API Key** (⭐ Recommended - Simpler, faster setup)
2. **Traditional AWS Credentials** (Access Key + Secret Key via AWS CLI)

**This guide shows BOTH methods. Choose the one that works best for you.**

---

# Method 1: AWS Bedrock API Key (Recommended - Simplest)

This is the **fastest and easiest** way to get started. No AWS CLI needed!

## Step 1: Enable AWS Bedrock Access

### 1.1 Request Bedrock Access (If First Time)

1. Sign in to AWS Console: https://console.aws.amazon.com/
2. Navigate to **AWS Bedrock** service
3. If you see a "Request Access" message, click to request access
4. AWS typically grants access within 1-2 business days

### 1.2 Enable Claude Models

1. Go to AWS Bedrock Console: https://console.aws.amazon.com/bedrock/
2. In the left sidebar, click **"Model access"**
3. Click **"Enable specific models"** or **"Manage model access"**
4. Find and enable these models:
   - ✅ **Claude Opus 4.5** (`us.anthropic.claude-opus-4-5-20251101-v1:0`) - For batch summaries
   - ✅ **Claude 3 Haiku** (`anthropic.claude-3-haiku-20240307-v1:0`) - For RAG queries (Phase 2)
   - ✅ **Titan Embeddings** (`amazon.titan-embed-text-v1`) - For vector embeddings (Phase 2)
5. Click **"Save changes"**
6. Wait 1-2 minutes for model access to be activated

**Note:** Model IDs may vary by region. The above IDs are for `us-east-1` (recommended region).

## Step 2: Generate AWS Bedrock API Key

### 2.1 Create API Key

1. In AWS Bedrock Console, click **"Settings"** in the left sidebar
2. Click **"API keys"** tab
3. Click **"Create API key"** button
4. Give your API key a name (e.g., "Survey Analysis Tool")
5. Click **"Create"**
6. **IMPORTANT:** Copy the API key immediately - you won't be able to see it again!
7. Store it securely (never commit to version control!)

### 2.2 Configure API Key in Your Project

**Option A: Using .env File (Recommended for local development)**

1. Copy the example environment file:
   ```bash
   copy .env.example .env
   ```

2. Open `.env` in a text editor and add your API key:
   ```
   AWS_BEARER_TOKEN_BEDROCK=your_actual_api_key_here
   ```

   **IMPORTANT:** Replace `your_actual_api_key_here` with the actual API key you copied from AWS Bedrock Console.

3. Save the file

**Option B: Using Environment Variables (For production/CI/CD or quick testing)**

**Windows (Command Prompt):**
```cmd
set AWS_BEARER_TOKEN_BEDROCK=your_actual_api_key_here
```

**Windows (PowerShell):**
```powershell
$env:AWS_BEARER_TOKEN_BEDROCK="your_actual_api_key_here"
```

**Mac/Linux:**
```bash
export AWS_BEARER_TOKEN_BEDROCK=your_actual_api_key_here
```

**Note:** Environment variables set in the terminal are temporary and only last for that session. For persistent configuration, use the `.env` file method (Option A).

## Step 3: Test Your Setup

### 3.1 Install Dependencies

```bash
pip install -r requirements.txt
```

### 3.2 Test Connection

Run the batch summarizer to test your API key:

```bash
python llm_batch_summarizer.py
```

Expected output:
```
✓ Using AWS Bedrock API Key authentication
✓ Initialized AWS Bedrock client with us.anthropic.claude-opus-4-5-20251101-v1:0
...
```

If you see this, you're all set! 🎉

### 3.3 Run the Dashboard

```bash
streamlit run app.py
```

Navigate to "🤖 AI Insights" tab and click "🚀 Generate AI Summaries"

---

# Method 2: Traditional AWS Credentials (Alternative)

If you prefer using AWS CLI or already have AWS credentials configured, use this method.

## Step 1: Enable AWS Bedrock Access

(Same as Method 1, Steps 1.1 and 1.2 above)

## Step 2: Configure IAM Permissions

### 2.1 Create IAM Policy for Bedrock

1. Go to IAM Console: https://console.aws.amazon.com/iam/
2. Click **"Policies"** → **"Create policy"**
3. Switch to **JSON** tab
4. Paste this policy:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel",
        "bedrock:InvokeModelWithResponseStream",
        "bedrock:ListFoundationModels",
        "bedrock:GetFoundationModel"
      ],
      "Resource": "*"
    }
  ]
}
```

5. Click **"Next: Tags"** (optional, skip if not needed)
6. Click **"Next: Review"**
7. Name the policy: `BedrockInvokeAccess`
8. Click **"Create policy"**

### 2.2 Attach Policy to Your User

1. Go to **IAM → Users**
2. Click on your username
3. Click **"Add permissions"** → **"Attach policies directly"**
4. Search for `BedrockInvokeAccess`
5. Select the checkbox and click **"Next"** → **"Add permissions"**

## Step 3: Install and Configure AWS CLI

### 3.1 Install AWS CLI

**Windows:**
```bash
winget install Amazon.AWSCLI
```

**Mac:**
```bash
brew install awscli
```

**Linux:**
```bash
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```

### 3.2 Configure Credentials

Run:
```bash
aws configure
```

Enter:
- **AWS Access Key ID:** [Your access key]
- **AWS Secret Access Key:** [Your secret key]
- **Default region name:** `us-east-1`
- **Default output format:** `json`

**To get your access keys:**
1. Go to IAM Console → Users → Your username
2. Click **"Security credentials"** tab
3. Scroll to **"Access keys"**
4. Click **"Create access key"**
5. Select **"Command Line Interface (CLI)"**
6. Copy the Access Key ID and Secret Access Key

### 3.3 Verify Configuration

```bash
aws bedrock list-foundation-models --region us-east-1
```

You should see a JSON list of available models.

## Step 4: Test Your Setup

```bash
python llm_batch_summarizer.py
```

Expected output:
```
✓ Using traditional AWS credentials
✓ Initialized AWS Bedrock client with us.anthropic.claude-opus-4-5-20251101-v1:0
...
```

---

# Cost Monitoring

## Set Up Budgets

1. Go to AWS Billing Console: https://console.aws.amazon.com/billing/
2. Click **"Budgets"** → **"Create budget"**
3. Select **"Cost budget"**
4. Set budget amount: **$10/month**
5. Configure alerts:
   - Alert at 50% ($5)
   - Alert at 80% ($8)
   - Alert at 100% ($10)
6. Enter your email for notifications

## Estimated Costs

**Phase 1: Batch Summarization (Opus 4.5)**

- Input: $15/1M tokens
- Output: $75/1M tokens

**Per full survey run:**
- 12 questions + overall summary = **~$2.08 per run**

**Monthly cost (weekly regeneration):**
- 4 runs × $2.08 = **~$8.32/month**

**Phase 2: RAG with Haiku (when implemented):**
- 100 queries/month = **~$0.08/month**

**Total: ~$8.40/month** (well within budget!)

## Monitor Usage

View your Bedrock usage:

1. Go to AWS Cost Explorer: https://console.aws.amazon.com/cost-management/
2. Filter by **Service: Bedrock**
3. Set date range to **Last 30 days**

---

# Troubleshooting

### ❌ Error: "AccessDeniedException: User is not authorized to perform: bedrock:InvokeModel"

**Solution:**
- **API Key method:** Verify your API key is correct and not expired
- **Traditional method:** Check IAM policy is attached to your user
- Wait 5 minutes for permissions to propagate

### ❌ Error: "ValidationException: The provided model identifier is invalid"

**Solution:**
- Check model access is enabled in Bedrock console (Step 1.2)
- Verify model ID matches your region: `us.anthropic.claude-opus-4-5-20251101-v1:0`
- Try: `aws bedrock list-foundation-models --region us-east-1`

### ❌ Error: "ResourceNotFoundException: Could not find credentials"

**Solution:**
- **API Key method:** Check `AWS_BEARER_TOKEN_BEDROCK` environment variable is set
- **Traditional method:** Run `aws configure` to set up credentials

### ❌ Error: "Could not connect to the endpoint URL"

**Solution:**
- Bedrock is not available in all regions - use `us-east-1` (recommended)
- Set region explicitly: `export AWS_REGION=us-east-1`

### ❌ Error: "ThrottlingException: Rate exceeded"

**Solution:**
- Bedrock has rate limits (varies by model)
- The batch summarizer includes delays between requests
- If still throttled, wait a few minutes and retry

### 💰 Cost Concerns

**To reduce costs:**
- Generate summaries less frequently (monthly vs weekly)
- Use Haiku instead of Opus for less critical summaries (10x cheaper but lower quality)
- Cache summaries (don't regenerate unless data changes)
- Set strict AWS Budgets with email alerts

---

# Security Best Practices

### 1. Never Commit API Keys or Credentials

The `.gitignore` file already includes:
```
.env
llm_summaries.json
chroma_db/
```

**Always:**
- Use `.env` files for local development
- Use environment variables for production
- Never commit `.env` to version control
- Rotate API keys every 90 days

### 2. Use IAM Roles (When Possible)

For production deployments (EC2, ECS, Lambda):
- Use IAM roles instead of API keys
- Roles automatically rotate credentials
- No need to store keys

### 3. Enable CloudTrail Logging

Track all Bedrock API calls for security auditing:
1. Go to CloudTrail console
2. Create a trail
3. Enable logging for Bedrock service

---

# Region Selection

AWS Bedrock model availability varies by region:

- ✅ **us-east-1 (N. Virginia)** - Best model availability (Recommended)
- ✅ **us-west-2 (Oregon)** - Good availability
- ✅ **eu-west-1 (Ireland)** - For European users

Check model availability:
```bash
aws bedrock list-foundation-models --region us-east-1 --query 'modelSummaries[?contains(modelId, `claude`)].modelId'
```

---

# Next Steps

Once AWS Bedrock is configured:

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Test the batch summarizer:**
   ```bash
   python llm_batch_summarizer.py
   ```

3. **Run the Streamlit dashboard:**
   ```bash
   streamlit run app.py
   ```
   → Go to "🤖 AI Insights" tab

4. **Generate your first summaries!** 🎉

---

# Support Resources

- **AWS Bedrock Documentation:** https://docs.aws.amazon.com/bedrock/
- **Anthropic Claude Documentation:** https://docs.anthropic.com/
- **AWS CLI Reference:** https://docs.aws.amazon.com/cli/
- **boto3 Documentation:** https://boto3.amazonaws.com/v1/documentation/api/latest/

---

**Questions?** Check the troubleshooting section above or refer to the official AWS Bedrock documentation.
