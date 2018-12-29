# coding: utf-8

import numpy as np
import pandas as pd
from typing import Iterable, Any
from functools import partial






def convert_na_values(df: pd.DataFrame, value: Any = None) -> pd.DataFrame:
    """ Конвертировать все типы <numpy/pandas> в типы Python
            (например можно использовать перед сериализацией в json)
    """

    # noinspection PyUnresolvedReferences
    result = df.astype(object).where(df.notnull(), value)
    return result





def cartesian_product(
    arrays: Iterable[Iterable],
    dtype=None,
    try_type_conversion: bool = False,
    verbose_mode: bool = True

) -> np.array:

    """ Декартово произведение

        :param arrays: Входная матрица в виде списка списков
        :param dtype: Тип данных в <arrays>
        :param try_type_conversion: При возникновении ошибки попытаться выполнить процедуру с конвертирование dtype=object
        :type verbose_mode: Подробный вывод
    """

    def _apply(dtype):
        res = np.empty_like(ix, dtype=dtype)
        for n, arr in enumerate(arrays):
            res[:, n] = arrays[n][ix[:, n]]

        return res


    arrays = list(map(
        np.asarray,
        (
            x if isinstance(x, Iterable) and not isinstance(x, str) else [x, ]
            for x in arrays
        )
    ))

    shape = map(len, arrays)
    dtype = dtype or arrays[0].dtype

    ix = np.indices(shape)
    ix = ix.reshape(len(arrays), -1).T


    try:
        results = _apply(dtype=dtype)

    except (TypeError, ValueError) as e:
        if try_type_conversion:
            results = _apply(dtype='object')
            if verbose_mode:
                print(e)

        else: raise e

    return results




def explode_dataframe_rows(X: pd.DataFrame, dtype=None, try_type_conversion=False, verbose_mode=True) -> pd.DataFrame:
    """ Разбивка ("разрыв") строк DataFrame, где элементы - массивы, на новые строки
        (на основе последовательного Декартового произведения элементов(массивов) каждой исходной строки)

        >>> df = pd.DataFrame({'A': [np.nan, [1, 2]], 'B': [[11, 22], 'first']})
        >>> print(df)
             A         B
        0  [1]  [22, 33]
        1  [5]      [55]

        >>> print(explode_dataframe_rows(df, dtype=float, try_type_conversion=True, verbose_mode=False))
             A      B
        0  NaN     11
        1  NaN     22
        2    1  first
        3    2  first
    """

    ### Если не сделать проверку на НЕпустой <DataFrame>, то полезут ошибки в функциях <numpy>
    if not X.empty:
        extended_rows = np.vstack(X.apply(
            ### все элементы должны быть массивами для корректной работы <cartesian>
            partial(cartesian_product, dtype=dtype, try_type_conversion=try_type_conversion, verbose_mode=verbose_mode),
            axis=1
        ))
        result = pd.DataFrame(extended_rows, columns=X.columns)

    else: result = pd.DataFrame()

    return result