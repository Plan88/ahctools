use svg::node::element::{Circle, Group, Line, Rectangle, Text, Title};
use svg::node::Text as TextContent;

pub fn rectangle(x: usize, y: usize, width: usize, height: usize, fill: &str) -> Rectangle {
    Rectangle::new()
        .set("x", x)
        .set("y", y)
        .set("width", width)
        .set("height", height)
        .set("fill", fill)
}

pub fn stroke_rectangle(
    x: usize,
    y: usize,
    width: usize,
    height: usize,
    fill: &str,
    stroke_width: usize,
) -> Rectangle {
    Rectangle::new()
        .set("x", x)
        .set("y", y)
        .set("width", width)
        .set("height", height)
        .set("fill", fill)
        .set("stroke", "gray")
        .set("stroke-width", stroke_width)
}

pub fn circle(x: usize, y: usize, r: usize, fill: &str) -> Circle {
    Circle::new()
        .set("cx", x)
        .set("cy", y)
        .set("r", r)
        .set("fill", fill)
}

pub fn line(x1: usize, y1: usize, x2: usize, y2: usize, color: &str) -> Line {
    Line::new()
        .set("x1", x1)
        .set("y1", y1)
        .set("x2", x2)
        .set("y2", y2)
        .set("stroke", color)
        .set("stroke-width", 3)
        .set("stroke-linecap", "round")
}

pub fn text(x: usize, y: usize, txt: &str, fontsize: usize) -> Text {
    Text::new()
        .add(TextContent::new(txt))
        .set("x", x)
        .set("y", y)
        .set("fill", "black")
        .set("font-size", fontsize)
        .set("dominant-baseline", "central")
        .set("text-anchor", "middle")
}

pub fn color(mut val: f64) -> String {
    val = val.clamp(0.0, 1.0);

    let (r, g, b) = if val < 0.5 {
        let x = val * 2.0;
        (
            30. * (1.0 - x) + 144. * x,
            144. * (1.0 - x) + 255. * x,
            255. * (1.0 - x) + 30. * x,
        )
    } else {
        let x = val * 2.0 - 1.0;
        (
            144. * (1.0 - x) + 255. * x,
            255. * (1.0 - x) + 30. * x,
            30. * (1.0 - x) + 70. * x,
        )
    };
    format!(
        "#{:02x}{:02x}{:02x}",
        r.round() as i32,
        g.round() as i32,
        b.round() as i32
    )
}

pub fn group(hoverinfo: String) -> Group {
    Group::new().add(Title::new().add(TextContent::new(hoverinfo)))
}
