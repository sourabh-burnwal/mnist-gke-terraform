provider "google" {
  credentials = file("/home/sourabh_root/Documents/Personal/projects/mnist/repo/FastAPI/infra/personal-427519-764ac84abb00.json")
  project     = "personal-427519"
  region      = "us-central1"
}