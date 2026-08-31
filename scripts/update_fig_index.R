# Refresh BIOS-SCOPE figure archive links and latest previews.
update_fig_index <- function(repo_root = ".") {
  repo_root <- normalizePath(repo_root, mustWork = TRUE)
  figs <- file.path(repo_root, "figs")
  dir.create(figs, recursive = TRUE, showWarnings = FALSE)
  archives <- list.dirs(figs, full.names = FALSE, recursive = FALSE)
  archives <- archives[grepl("^satellite_composites_[0-9]{8}$", archives)]
  archives <- sort(archives, decreasing = TRUE)
  latest <- file.path(figs, "latest_sat")
  if (dir.exists(latest)) unlink(latest, recursive = TRUE, force = TRUE)
  dir.create(latest, recursive = TRUE, showWarnings = FALSE)
  if (length(archives)) {
    files <- list.files(file.path(figs, archives[1]), pattern = "\\.(png|pdf)$", full.names = TRUE)
    file.copy(files, latest, overwrite = TRUE)
  }
  md <- c("# Figure archives", "", "- [Latest satellite products](latest_sat/)", "")
  for (a in archives) md <- c(md, paste0("- [", a, "](", a, "/)"))
  writeLines(md, file.path(figs, "README.md"))
  invisible(TRUE)
}

if (identical(environment(), globalenv())) update_fig_index(".")
