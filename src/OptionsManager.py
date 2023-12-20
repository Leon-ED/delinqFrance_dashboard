def needs_reduced_data_frame(*args):
    """
    needs_reduced_data_frame(*rgs)
    ------
    Vérifie si le DataFrame doit être réduit.
    Args:
    ------
        - *args (tuple):
            Tuple contenant les arguments de la fonction.
    Returns:
    ------
        - True si le DataFrame doit être réduit.
        - False sinon.
    """
    return any(arg != 'Tout' for arg in args)
     
     

    