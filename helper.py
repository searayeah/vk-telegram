from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)


def set_keyboard_7(
    a,
    callback_a,
    b,
    callback_b,
    c,
    callback_c,
    d,
    callback_d,
    e,
    callback_e,
    f,
    callback_f,
    g,
    callback_g,
):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(a, callback_data=str(callback_a)),
                InlineKeyboardButton(b, callback_data=str(callback_b)),
            ],
            [
                InlineKeyboardButton(c, callback_data=str(callback_c)),
                InlineKeyboardButton(d, callback_data=str(callback_d)),
            ],
            [
                InlineKeyboardButton(e, callback_data=str(callback_e)),
                InlineKeyboardButton(f, callback_data=str(callback_f)),
            ],
            [
                InlineKeyboardButton(g, callback_data=str(callback_g)),
            ],
        ]
    )


def set_keyboard_8(
    a,
    callback_a,
    b,
    callback_b,
    c,
    callback_c,
    d,
    callback_d,
    e,
    callback_e,
    f,
    callback_f,
    g,
    callback_g,
    h,
    callback_h,
):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(a, callback_data=str(callback_a)),
                InlineKeyboardButton(b, callback_data=str(callback_b)),
            ],
            [
                InlineKeyboardButton(c, callback_data=str(callback_c)),
                InlineKeyboardButton(d, callback_data=str(callback_d)),
            ],
            [
                InlineKeyboardButton(e, callback_data=str(callback_e)),
                InlineKeyboardButton(f, callback_data=str(callback_f)),
            ],
            [
                InlineKeyboardButton(g, callback_data=str(callback_g)),
                InlineKeyboardButton(h, callback_data=str(callback_h)),
            ],
        ]
    )


def set_keyboard_1(x, callback_x):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(x, callback_data=str(callback_x)),
            ],
        ]
    )


def set_keyboard_row_3(
    x,
    y,
    z,
    callback_x,
    callback_y,
    callback_z,
):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(x, callback_data=str(callback_x)),
                InlineKeyboardButton(y, callback_data=str(callback_y)),
                InlineKeyboardButton(z, callback_data=str(callback_z)),
            ]
        ]
    )


def set_keyboard_column_3(
    x,
    y,
    z,
    callback_x,
    callback_y,
    callback_z,
):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(x, callback_data=str(callback_x)),
            ],
            [
                InlineKeyboardButton(y, callback_data=str(callback_y)),
            ],
            [
                InlineKeyboardButton(z, callback_data=str(callback_z)),
            ],
        ]
    )


def set_keyboard_triangle_3(
    x,
    y,
    z,
    callback_x,
    callback_y,
    callback_z,
):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(x, callback_data=str(callback_x)),
                InlineKeyboardButton(y, callback_data=str(callback_y)),
            ],
            [
                InlineKeyboardButton(z, callback_data=str(callback_z)),
            ],
        ]
    )


def set_keyboard_square_4(
    x,
    y,
    z,
    t,
    callback_x,
    callback_y,
    callback_z,
    callback_t,
):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(x, callback_data=str(callback_x)),
                InlineKeyboardButton(y, callback_data=str(callback_y)),
            ],
            [
                InlineKeyboardButton(z, callback_data=str(callback_z)),
                InlineKeyboardButton(t, callback_data=str(callback_t)),
            ],
        ]
    )


def set_keyboard_square_5(
    x,
    y,
    z,
    t,
    s,
    callback_x,
    callback_y,
    callback_z,
    callback_t,
    callback_s,
):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(x, callback_data=str(callback_x)),
                InlineKeyboardButton(y, callback_data=str(callback_y)),
            ],
            [
                InlineKeyboardButton(z, callback_data=str(callback_z)),
                InlineKeyboardButton(t, callback_data=str(callback_t)),
            ],
            [
                InlineKeyboardButton(s, callback_data=str(callback_s)),
            ],
        ]
    )
