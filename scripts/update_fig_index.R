# Refresh BIOS-SCOPE figure archives and latest-product folders.
update_fig_index <- function(repo_root = ".", add_thumbnails = TRUE, do_git = FALSE) {
  repo_root <- normalizePath(repo_root, mustWork = TRUE)
  figs <- file.path(repo_root, "figs")
  dir.create(figs, recursive = TRUE, showWarnings = FALSE)

  newest_archive <- function(pattern) {
    hits <- list.dirs(figs, full.names = FALSE, recursive = FALSE)
    hits <- sort(hits[grepl(pattern, hits)], decreasing = TRUE)
    if (length(hits)) hits[1] else NULL
  }

  copy_archive <- function(archive, destination) {
    if (dir.exists(destination)) unlink(destination, recursive = TRUE, force = TRUE)
    dir.create(destination, recursive = TRUE, showWarnings = FALSE)
    if (is.null(archive)) return(invisible(FALSE))
    files <- list.files(
      file.path(figs, archive), pattern = "\\.(png|pdf)$",
      full.names = TRUE, ignore.case = TRUE
    )
    if (length(files)) file.copy(files, destination, overwrite = TRUE)
    invisible(length(files) > 0)
  }

  newest_sat <- newest_archive("^satellite_composites_[0-9]{8}$")
  newest_float <- newest_archive("^float_composites_[0-9]{8}$")

  copy_archive(newest_sat, file.path(figs, "latest_sat"))
  copy_archive(newest_float, file.path(figs, "latest_float"))
  copy_archive(newest_sat, file.path(figs, "latest", "satellite"))
  copy_archive(newest_float, file.path(figs, "latest", "float"))

  archives <- list.dirs(figs, full.names = FALSE, recursive = FALSE)
  archives <- sort(
    archives[grepl("^(satellite|float)_composites_[0-9]{8}$", archives)],
    decreasing = TRUE
  )

  md <- c(
    "# Figure archives", "",
    "- [Latest satellite products](latest_sat/)",
    "- [Latest float products](latest_float/)", ""
  )
  for (archive in archives) {
    md <- c(md, paste0("- [", archive, "](", archive, "/)"))
    if (isTRUE(add_thumbnails)) {
      images <- list.files(file.path(figs, archive), pattern = "\\.png$", ignore.case = TRUE)
      if (length(images)) {
        md <- c(md, paste0("  ![](", archive, "/", head(images, 4), ")"))
      }
    }
  }
  writeLines(md, file.path(figs, "README.md"))

  if (isTRUE(do_git)) {
    message("Figure index updated. Git actions are intentionally left to the user.")
  }
  invisible(TRUE)
}
