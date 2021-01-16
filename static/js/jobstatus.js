function filter(type) {
    if (type == "location") {
      $(`.${type}`).toggle();
    } else if (type == "experience") {
      $(`.${type}`).toggle();
    } else {
    $(`.${type}`).toggle();
    }
}

function shortlist(id) {
    window.open(`/jobads/${id}/shortlist`, "_self");
    $(".testing").prop("hidden", false);
}

function interview(id) {
    window.open(`/jobads/${id}/interview`, "_self");
}

function notsuitable(id) {
    window.open(`/jobads/${id}/notsuitable`, "_self");
}

function addToList(type) {
    if (type == "shortlist") {
        $('.nav-tabs a[href=".' + type + '"]').tab("show");
        $("#dataTable").append(
          '<tbody class="text-dark">' +
            "<tr>" +
            '<td class="font-weight-bold">10</td>' +
            "<td>Mark</td>" +
            "<td>makr124</td>" +
            '<td class="text-success">RM4,000</td>' +
            "<td>22/6/2020</td>" +
            "<td>" +
            '<button type="button" class="btn btn-primary">INTERVIEW</button>' +
            '<button type="button" class="btn btn-primary ml-2">NOT SUITABLE</button>' +
            "</td>" +
            "</tr>" +
            "</tbody>"
      );
    } else if (type == "interview") {
        $('.nav-tabs a[href=".' + type + '"]').tab("show");
        $(".interview .table").append(
          '<tbody class="text-dark">' +
            "<tr>" +
            '<td class="font-weight-bold">10</td>' +
            "<td>Mark</td>" +
            "<td>makr124</td>" +
            '<td class="text-success">RM4,000</td>' +
            "<td>22/6/2020</td>" +
            "<td>" +
            '<button type="button" class="btn btn-primary">SHORTLIST</button>' +
            '<button type="button" class="btn btn-primary ml-2">NOT SUITABLE</button>' +
            "</td>" +
            "</tr>" +
            "</tbody>"
      );
    } else if (type == "notsuitable") {
        $('.nav-tabs a[href=".' + type + '"]').tab("show");
        $(".notsuitable .table").append(
          '<tbody class="text-dark">' +
            "<tr>" +
            '<td class="font-weight-bold">10</td>' +
            "<td>Mark</td>" +
            "<td>makr124</td>" +
            '<td class="text-success">RM4,000</td>' +
            "<td>22/6/2020</td>" +
            "<td>" +
            '<button type="button" class="btn btn-danger">DELETE</button>' +
            "</td>" +
            "</tr>" +
            "</tbody>"
        );
    }
}
