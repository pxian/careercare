function expandFrame(type) {
    if (type == "click") {
        $(".click").modal('show');
    }
    else if (type == "apply") {
        $(".apply").modal('show');
    }
    else if (type == "rating") {
        $(".rating").modal('show');
    }
    else if (type == "keyword") {
        $(".keyword").modal('show');
    }
    else if (type == "jobs") {
        $(".jobs").modal('show');
    }
    else if (type == "salary") {
        $(".salary").modal('show');
    }
    else if (type == "status") {
        $(".status").modal('show');
    }
    else if (type == "competitor") {
        $(".competitor").modal('show');
    }
    else if (type == "demographics") {
        $(".demographics").modal('show');
    }
    else if (type == "talent") {
        $(".talent").modal('show');
    }
    else {
        $(".work").modal('show');
    }
}